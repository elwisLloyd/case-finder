# Fast graph-based layout detection

Источник: https://medium.com/lifen-engineering/fast-graph-based-layout-detection-19fc7ab11b17

Introduction
At Lifen we process medical PDF documents from thousands of clients. Those PDF documents come with a huge variety of layouts:
We need to perform layout detection from this 2D grid of words to produce a coherent 1D sequence. This 1D sequence can then be fed into our NLP models or sent as plain text when clients do not support PDF or image attachments.
Mistakes in this layout detection could result in nonsensical extracted text. This could mean for exemple mixing addresses of two recipients together.
Imagine in the left image above if we failed to understand that the green and yellow blocks are two columns that should be read one after the other: we would create sentences mixing pieces of text from both blocks.
Isn’t layout information already encoded in PDFs?
Most of the time, yes. There is a sense of order in the way it is encoded, but there are no means to be sure this is the case, and results can be pretty bad if we just trust PDFs blindly. Furthermore, in the case of images PDF (which needs OCR), there is no text order to recover.
Objective: be fast & accurate
Existing solutions
Existing solutions (such as pdfplumber, Parsr) use simple techniques such as XY cut¹ and did not perform well enough on our dataset. Furthermore, because accurate text extraction is critical for our product, we need to be able to constantly fine-tune our solution to be as accurate as possible with new clients. Existing solutions did not allow us the level of customization we needed.
Avoid OCR when possible
Multiple solutions combine OCR with layout detection. However, most of the documents we receive (~85%) have a clean extractable text and do not require OCR. Furthermore, doing OCR on every document we process would be slow and expensive we’re happy to avoid as much as we can. For image documents, we first apply OCR then use the extracted text as a starting point just as extractable PDFs.
Our solution
Previous work
There is an active community of research in the field of layout analysis, with academic conferences such as the International Conference on Document Analysis and Recognition. One resource we found particularly valuable to navigate this field is survey of algorithms².
However, while reviewing papers we found out that few share the characteristics we are looking for: start from extractable PDFs, fast and fine-tunable.
One great paper using the same starting point as us (no OCR, words and not pixels) and with great care for speed is Object-Level Document Analysis of PDF Files³. The idea is to build a graph of words, discard edges linking words from different paragraphs until the connected components left are the paragraphs. The ideas we took from this paper are:
- Reduce the number of words in linear time by merging words that without a doubt belong to the same line
- Build a graph as fast as possible by looking only for direct neighbors in the four directions.
- “Best-first clustering” algorithm: sort edges (mainly by length) and choose to discard them or not one by one by using previous decisions to make informed decisions on longer trickier edges.
However, the algorithms they use to sort edges and choose to discard them, are complex sequences of rules that we found difficult to fine-tune and maintain.
Get Jean-Charles Louis’s stories in your inbox
Join Medium for free to get updates from this writer.
From A Machine Learning Approach for Graph-Based Page Segmentation⁴, we took the idea of using a machine learning model to classify edges.
Bring everything together
1. Pre-processing
We’re extracting words and their positions using pdftotext --bbox-layout. This gives us a list of words in 2D grid and an estimation by pdftotext of word order (in an XML format similar to hOCR).
2. Build graph
We build the word graph using a custom implementation of the algorithm from³.
3. Give a should_merge score to each edge:
Using a manually tagged dataset, we train a Random Forest to give a should_merge score for each edge using features.
Features definitions:
- dist_font_size: distance between words in units of font_size (or mean font_size if not the same between words)
- xml_neighbours: neighbours according to PDF infos extracted by pdftotext (accurate ~90% of the time)
- nb_aligned_left: number of words aligned left with this word (does it looks like this word is on the left side of a paragraph)
3. Sort edges by should_merge score and keep certain
Using a threshold that gives us a precision of 1.00 during evaluation, we keep every edge that is “certain” (recall at this threshold is 0.75).
Our second threshold aims for a precision > 0.9, gives us “possible” edges.
Rest of edges are discarded.
4. Make decisions about “possible” edges using current state
Our random forest only sees two words at the time (but some features such as nb_aligned_left give more global context). For less obvious edges (with a lower should_merge score), we make decisions based on the current state of the layout. We compute a “stateful” coefficient that multiply the should_merge score.
For exemple, when considering an edge between two words from two clusters that seem to come from one same column, we increase the should_merge score.
Future work
At this point our library is too much integrated with the rest of our app to be split into an open-source solution. We are considering open-sourcing it in the future. In the meantime, do not hesitate to contact us if you want more details.
We’re also thinking of using a more end-to-end approach by combining the layout extraction with the downstream task directly in our NLP models. LayoutLM⁵ is a promising work in this direction.
References
[1] Hierarchical representation of optically scanned documents https://core.ac.uk/download/pdf/84308932.pdf
[2] A comprehensive survey of mostly textual document segmentation algorithms since 2008 https://hal.archives-ouvertes.fr/hal-01388088/document
[3] Object-Level Document Analysis of PDF Files https://www.dbai.tuwien.ac.at/staff/hassan/files/p47-hassan.pdf
[4] A Machine Learning Approach for Graph-Based Page Segmentation https://www.researchgate.net/publication/328719252_A_Machine_Learning_Approach_for_Graph-Based_Page_Segmentation
[5] LayoutLM: Pre-training of Text and Layout for Document Image Understanding https://arxiv.org/abs/1912.13318
