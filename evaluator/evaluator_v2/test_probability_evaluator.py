import json
import math
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import pandas as pd

from evaluator.evaluator_v2.probability_evaluator import (
    Assessment, Assessments, COLUMNS, DEFAULT_PRIOR, DISTRIBUTION, EFFORT,
    PRIOR, QUESTION, UNCERTAINTY, evaluate, load_menu, load_spec, metrics,
    save_results, top_questions,
)

BASE = Path(__file__).parent


def mark(i, information='none', p=None, evidence='', question='Какие требования нужны?'):
    return Assessment(item_id=i, information=information, p=p or list(DEFAULT_PRIOR),
                      evidence=evidence, question=question, comment='Обоснование оценки.')


class MetricsTests(unittest.TestCase):
    def test_methodology_example(self):
        result = metrics([.5, .3, .1, .1], 3, 1)
        self.assertAlmostEqual(result[EFFORT], 4.8)
        self.assertAlmostEqual(result[UNCERTAINTY], math.sqrt(77.76))
        self.assertEqual(result['Raw Priority'], result[UNCERTAINTY])
        self.assertEqual(result['Priority'], result[UNCERTAINTY])

    def test_point_and_extreme_distributions(self):
        for p, expected in [([0, 1, 0, 0], 5), ([1, 0, 0, 0], 0),
                            ([0, 0, 0, 1], 50)]:
            result = metrics(p, 5)
            self.assertEqual(result[EFFORT], expected)
            self.assertEqual(result[UNCERTAINTY], 0)
        result = metrics([.5, 0, 0, .5], 5, 4)
        self.assertEqual(result[UNCERTAINTY], 25)
        self.assertEqual(result['Priority'], 12.5)

    def test_invalid_inputs_fail(self):
        for p in [[1, 1, 0, 0], [1, 0, 0], [-.1, 1.1, 0, 0],
                  [float('nan'), 0, 0, 1], [True, 0, 0, 0]]:
            with self.subTest(p=p), self.assertRaises(ValueError):
                metrics(p, 3)
        for k, c in [(0, 2), (3, 0), (float('inf'), 2), (3, -1)]:
            with self.assertRaises(ValueError):
                metrics([1, 0, 0, 0], k, c)


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.menu = load_menu(BASE / 'chatbots_menu.csv')

    def test_all_menu_rows(self):
        self.assertEqual(len(self.menu), 42)
        for _, row in self.menu.iterrows():
            result = metrics(json.loads(row[PRIOR]), row['Коэффициент трудоемкости'],
                             row['Стоимость уточнения'])
            self.assertGreaterEqual(result['Priority'], 0)

    def test_partial_explicit_prior_progress_and_export(self):
        menu = self.menu.head(3)
        text = 'Нужен стандартный виджет. Каналы пока обсуждаются.'
        answers = [Assessments(items=[
            mark(0, 'explicit', [0, 1, 0, 0], 'Нужен стандартный виджет.'),
            # Deliberately wrong model p with information=none: Python must use q.
            mark(1, p=[1, 0, 0, 0]),
        ]), Assessments(items=[mark(2, 'partial', [.1, .6, .25, .05],
                                   'Каналы пока обсуждаются.')])]
        calls = []
        with patch('evaluator.evaluator_v2.probability_evaluator.ask', side_effect=answers):
            result = evaluate(None, 'test', menu, text, batch_size=2,
                              progress=lambda done, total: calls.append((done, total)))
        self.assertEqual(calls, [(0, 3), (2, 3), (3, 3)])
        self.assertEqual(list(result), COLUMNS)
        self.assertTrue(result['Priority'].is_monotonic_decreasing)
        by_name = result.set_index('Компонент')
        explicit = by_name.loc[menu.iloc[0]['Компонент']]
        self.assertEqual(explicit[QUESTION], '')
        self.assertEqual(explicit[UNCERTAINTY], 0)
        absent = by_name.loc[menu.iloc[1]['Компонент']]
        self.assertEqual(json.loads(absent[DISTRIBUTION]), json.loads(menu.iloc[1][PRIOR]))
        self.assertEqual(len(top_questions(result)), 2)
        with TemporaryDirectory() as tmp:
            path = save_results(result, tmp, 'тест')
            self.assertTrue(path.read_bytes().startswith(b'\xef\xbb\xbf'))
            exported = pd.read_csv(path)
            self.assertEqual(list(exported), COLUMNS)
            self.assertEqual(len(exported), 3)
            self.assertTrue(exported['Priority'].is_monotonic_decreasing)

    def test_missing_duplicate_and_unknown_ids(self):
        for items in [[], [mark(0), mark(0)], [mark(0), mark(8)]]:
            with self.subTest(items=items):
                with patch('evaluator.evaluator_v2.probability_evaluator.ask',
                           return_value=Assessments(items=items)):
                    with self.assertRaises(ValueError):
                        evaluate(None, 'test', self.menu.head(2), 'ТЗ', progress=lambda *_: None)

    def test_fabricated_quote_and_missing_question_fail(self):
        for assessment in [mark(0, 'partial', evidence='Выдуманная цитата'),
                           mark(0, question=' ')]:
            with patch('evaluator.evaluator_v2.probability_evaluator.ask',
                       return_value=Assessments(items=[assessment])):
                with self.assertRaises(ValueError):
                    evaluate(None, 'test', self.menu.head(1), 'Настоящее ТЗ', progress=lambda *_: None)

    def test_defaults_and_bad_menu(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / 'menu.csv'
            original = self.menu.head(1).drop(columns=[PRIOR, 'Стоимость уточнения'])
            original.to_csv(path, index=False)
            loaded = load_menu(path)
            self.assertEqual(json.loads(loaded.iloc[0][PRIOR]), list(DEFAULT_PRIOR))
            self.assertEqual(float(loaded.iloc[0]['Стоимость уточнения']), 2)
            original['Оценка Small, чел.-дн.'] = '999'
            original.to_csv(path, index=False)
            with self.assertRaises(ValueError):
                load_menu(path)

    def test_api_refusal(self):
        from evaluator.evaluator_v2.probability_evaluator import ask
        client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(
            parse=lambda **_: SimpleNamespace(choices=[SimpleNamespace(
                message=SimpleNamespace(refusal='refused', parsed=None))]))))
        with self.assertRaises(RuntimeError):
            ask(client, 'test', Assessments, 'task', {})

    def test_full_text_no_truncation_and_paths(self):
        with patch('evaluator.evaluator_v2.probability_evaluator.ask') as api:
            with self.assertRaises(ValueError):
                evaluate(None, 'test', self.menu, 'a' * 100, max_spec_chars=99)
            api.assert_not_called()
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            tz = root / 'TZ'
            tz.mkdir()
            spec = tz / 'spec.md'
            spec.write_text('Полное ТЗ', encoding='utf-8')
            self.assertEqual(load_spec(spec, tz), 'Полное ТЗ')
            outside = root / 'outside.md'
            outside.write_text('ТЗ', encoding='utf-8')
            with self.assertRaises(ValueError):
                load_spec(outside, tz)


class ValidationRetryTests(unittest.TestCase):
    def make_client(self, responses):
        responses = iter(responses)

        def parse(**kwargs):
            # Как в OpenAI SDK: Pydantic разбирает JSON внутри completions.parse.
            parsed = kwargs['response_format'].model_validate_json(next(responses))
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(
                refusal=None, parsed=parsed))])

        parse_mock = Mock(side_effect=parse)
        client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(parse=parse_mock)))
        return client, parse_mock

    def response_json(self, information):
        return json.dumps({'items': [{
            'item_id': 0, 'information': information, 'p': [0, .8, .2, 0],
            'evidence': 'Стандартный виджет.',
            'question': 'Нужна ли кастомизация интерфейса?',
            'comment': 'Уровень зависит от кастомизации.',
        }]}, ensure_ascii=False)

    def test_sdk_validation_error_is_repaired_without_losing_probabilities(self):
        from evaluator.evaluator_v2.probability_evaluator import ask
        client, parse = self.make_client([
            self.response_json('explicit'), self.response_json('partial')])
        with patch('builtins.print'):
            result = ask(client, 'test', Assessments, 'Оцени пакет.', {'ТЗ': 'Стандартный виджет.'})
        self.assertEqual(parse.call_count, 2)
        self.assertEqual(result.items[0].information, 'partial')
        self.assertEqual(result.items[0].p, [0, .8, .2, 0])
        first, second = parse.call_args_list
        self.assertEqual(first.kwargs['messages'][1], second.kwargs['messages'][1])
        self.assertIn('items.0', second.kwargs['messages'][0]['content'])
        self.assertIn('Не делай оценку однозначной', second.kwargs['messages'][0]['content'])

    def test_invalid_answer_stops_after_three_attempts(self):
        from evaluator.evaluator_v2.probability_evaluator import ask
        client, parse = self.make_client([self.response_json('explicit')] * 3)
        with patch('builtins.print'), self.assertRaisesRegex(RuntimeError, 'за 3 попытки'):
            ask(client, 'test', Assessments, 'Оцени пакет.', {})
        self.assertEqual(parse.call_count, 3)

    def test_valid_response_is_not_repeated(self):
        from evaluator.evaluator_v2.probability_evaluator import ask
        client, parse = self.make_client([self.response_json('partial')])
        ask(client, 'test', Assessments, 'Оцени пакет.', {})
        self.assertEqual(parse.call_count, 1)

    def test_transport_failure_is_not_treated_as_validation(self):
        from evaluator.evaluator_v2.probability_evaluator import ask
        client, parse = self.make_client([])
        parse.side_effect = ConnectionError('API недоступен')
        with self.assertRaises(ConnectionError):
            ask(client, 'test', Assessments, 'Оцени пакет.', {})
        self.assertEqual(parse.call_count, 1)

    def test_repaired_response_completes_evaluation(self):
        menu = load_menu(BASE / 'chatbots_menu.csv').head(1)
        client, parse = self.make_client([
            self.response_json('explicit'), self.response_json('partial')])
        with patch('builtins.print'):
            results = evaluate(client, 'test', menu, 'Стандартный виджет.', progress=lambda *_: None)
        self.assertEqual(len(results), 1)
        self.assertGreater(results.iloc[0][UNCERTAINTY], 0)
        self.assertTrue(results.iloc[0][QUESTION])
        self.assertEqual(parse.call_count, 2)


if __name__ == '__main__':
    unittest.main()
