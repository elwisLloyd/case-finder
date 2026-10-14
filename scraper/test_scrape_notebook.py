"""Offline tests: python -m unittest discover -s scraper -p 'test_*.py'.

Requires httpx. Extraction libraries are mocked: these tests verify orchestration,
not trafilatura/PyMuPDF extraction quality on live sources.
"""
import asyncio
import csv
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx


class NotebookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        notebook = json.loads(Path(__file__).with_name('scrape_use_cases.ipynb').read_text())
        code = '\n'.join(''.join(c['source']) for c in notebook['cells']
                         if c['cell_type'] == 'code' and not ''.join(c['source']).startswith(('%pip', 'counts = await', 'import subprocess')))
        self.ns = {}
        with patch.dict(sys.modules, {'trafilatura': types.SimpleNamespace(extract=lambda data, **kw: data.decode()),
                                      'pymupdf': types.SimpleNamespace()}):
            exec(compile(code, 'notebook', 'exec'), self.ns)
        root = Path(self.tmp.name)
        self.ns.update(BASE_DIR=root, CSV_PATH=root / 'input.csv', OUTPUT_DIR=root / 'scraped',
                       LOG_PATH=root / 'log.csv', REQUEST_PAUSE=0, USE_BROWSER=False)

    def test_403_browser_success_failure_and_disabled(self):
        with self.ns['CSV_PATH'].open('w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Link'])
            writer.writerow(['Blocked article', 'https://example.org/blocked'])
        request = httpx.Request('GET', 'https://example.org/redirected')
        response = httpx.Response(403, request=request)
        def blocked(client, url):
            raise httpx.HTTPStatusError('Forbidden', request=request, response=response)
        self.ns['fetch'] = blocked
        calls = []
        async def browser(url):
            calls.append(url)
            return 'article text ' * 100, 'https://example.org/final'
        self.ns['browser_text'] = browser
        self.ns.update(USE_BROWSER=True, RESUME=False)
        self.assertEqual(asyncio.run(self.ns['run']())['успешно'], 1)
        self.assertEqual(calls, ['https://example.org/redirected'])
        with self.ns['LOG_PATH'].open(encoding='utf-8-sig') as f:
            self.assertEqual(list(csv.DictReader(f))[-1]['final_url'], 'https://example.org/final')
        async def denied(url):
            raise ValueError('HTTP 403 in browser')
        self.ns['browser_text'] = denied
        self.assertEqual(asyncio.run(self.ns['run']())['ошибка'], 1)
        with self.ns['LOG_PATH'].open(encoding='utf-8-sig') as f:
            self.assertIn('браузерная попытка не удалась', list(csv.DictReader(f))[-1]['error'])
        calls.clear()
        self.ns.update(USE_BROWSER=False, browser_text=browser)
        self.assertEqual(asyncio.run(self.ns['run']())['ошибка'], 1)
        self.assertEqual(calls, [])

    def test_captcha_not_saved(self):
        with self.ns['CSV_PATH'].open('w', encoding='utf-8', newline='') as f:
            f.write('Title,Link\nBlocked,https://example.org/article\n')
        self.ns['fetch'] = lambda client, url: ('html', b'Verify you are human CAPTCHA', url)
        self.assertEqual(asyncio.run(self.ns['run']())['ошибка'], 1)
        self.assertEqual(list(self.ns['OUTPUT_DIR'].glob('*.md')), [])

    def client(self, handler):
        return httpx.Client(transport=httpx.MockTransport(handler), follow_redirects=True)

    def test_retry_and_pdf_signature(self):
        calls = []
        def handler(request):
            calls.append(request)
            return httpx.Response(503) if len(calls) == 1 else httpx.Response(200, content=b'%PDF-1.7 test')
        with self.client(handler) as client, patch('time.sleep'):
            self.assertEqual(self.ns['fetch'](client, 'https://example.org/document')[0], 'pdf')
        self.assertEqual(len(calls), 2)

    def test_404_no_retry_and_skip_binary(self):
        calls = []
        def handler(request):
            calls.append(request)
            return httpx.Response(404)
        with self.client(handler) as client:
            with self.assertRaises(httpx.HTTPStatusError):
                self.ns['fetch'](client, 'https://example.org/missing')
        self.assertEqual(len(calls), 1)
        with self.client(lambda r: httpx.Response(200, headers={'content-type': 'video/mp4'})) as client:
            with self.assertRaises(self.ns['SkipSource']):
                self.ns['fetch'](client, 'https://example.org/watch')

    def test_size_limit(self):
        self.ns['MAX_BYTES'] = 3
        with self.client(lambda r: httpx.Response(200, headers={'content-type': 'text/html'}, content=b'large')) as client:
            with self.assertRaises(ValueError):
                self.ns['fetch'](client, 'https://example.org/article')

    def test_statuses_log_and_resume(self):
        with self.ns['CSV_PATH'].open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Link'])
            writer.writerows([['Article one', 'https://example.org/good'], ['Short article', 'https://example.org/short'],
                             ['Video', 'https://youtu.be/id'], ['Empty', 'https://example.org/empty']])
        calls = []
        def fetch(client, url):
            calls.append(url)
            text = 'article text ' * 100 if url.endswith('good') else ('short' if url.endswith('short') else '')
            return 'html', text.encode(), url
        self.ns['fetch'] = fetch
        counts = asyncio.run(self.ns['run']())
        self.assertEqual(dict(counts), {'успешно': 1, 'требует проверки': 1, 'пропущено': 1, 'ошибка': 1})
        self.assertTrue((self.ns['OUTPUT_DIR'] / '0001_Article_one.md').exists())
        self.assertTrue((self.ns['OUTPUT_DIR'] / '0002_Short_article.md').exists())
        with self.ns['LOG_PATH'].open(encoding='utf-8-sig') as f:
            log = list(csv.DictReader(f))
        self.assertIn('Короткий текст', log[1]['error'])
        calls.clear()
        asyncio.run(self.ns['run']())
        self.assertEqual(calls, ['https://example.org/empty'])
        self.ns['RETRY_REVIEW'] = True
        calls.clear()
        asyncio.run(self.ns['run']())
        self.assertEqual(calls, ['https://example.org/short', 'https://example.org/empty'])

    def test_filename_and_url_validation(self):
        name = self.ns['filename'](5, 'A / title\u202fwith spaces ' + 'я' * 300)
        self.assertTrue(name.startswith('0005_A_title_with_spaces_'))
        self.assertLess(len(name.encode()), 200)
        with self.assertRaises(self.ns['SkipSource']):
            self.ns['validate_url']('https://www.youtube.com/watch?v=1')
        with self.assertRaises(ValueError):
            self.ns['validate_url']('file:///etc/hosts')


if __name__ == '__main__':
    unittest.main()
