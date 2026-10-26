# Case Finder

This project uses OpenAI models to generate clarification questions for a new ML/AI use case in two ways:

1. from the new use-case text alone; and
2. from that text plus genuinely relevant cases retrieved from the training collection.

The second path summarizes and embeds the input, retrieves five nearest summaries, asks an LLM to remove false positives, and then supplies the complete text of the remaining cases to the question-generation prompt. The notebooks display both question lists separately so they can be evaluated later.

## Project layout

- `prepare-train-data.ipynb` builds the searchable training index.
- `find-case.ipynb` retrieves related cases and generates both question lists.
- `prompts.py` contains every LLM prompt in English and is shared by both notebooks.
- `data/train/files/` contains the training cases as Markdown files.
- `data/train/train_index.csv` is generated locally and contains `id`, `summary`, and `embedding` columns.
- `server/` contains the Docker Compose-based FastAPI service and its deployment instructions.

## Setup

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set `OPENAI_API_KEY`. You may also change the LLM model, embedding model, and retrieval candidate count there. Keep the same embedding model when building and querying an index; rebuilding the index is required after changing it. OpenAI API usage may incur charges.

Start Jupyter from the repository root so the relative data paths resolve correctly:

```bash
jupyter lab
```

## Build the training index

Open `prepare-train-data.ipynb` and run all cells. For every Markdown file under `data/train/files`, the notebook:

1. creates a one-paragraph summary with `OPENAI_LLM_MODEL`;
2. embeds that summary with `OPENAI_EMBEDDING_MODEL`; and
3. writes `data/train/train_index.csv` with the columns `id`, `summary`, and `embedding`.

The embedding is stored as a JSON array inside the CSV. The notebook saves after every processed case and resumes from existing rows, so rerunning it does not repeat successful API requests. Set `REBUILD_INDEX = True` in the configuration cell to regenerate every row (for example, after changing a prompt or model).

## Find cases and generate questions

First build the index. Then open `find-case.ipynb`, replace `USE_CASE_TEXT` in the input cell, and run all cells. The notebook will:

1. generate baseline clarification questions using only the input;
2. summarize and embed the input using the same shared prompt and configured models as indexing;
3. calculate cosine similarity and select the top five candidates;
4. have the LLM retain only semantically relevant candidates based on their summaries; and
5. generate enriched clarification questions from the target plus the complete text of retained cases.

The retrieval table, LLM relevance decisions, baseline questions, and enriched questions remain available as notebook variables for inspection. If no candidate passes relevance filtering, the enriched stage still runs with an explicit statement that no relevant reference was found.

The final section evaluates the two approaches on every Markdown file in `data/test/files/`.
For each case it generates both question lists, randomly presents them as lists A and B to an LLM
acting as the customer, and records which list appears more professional and demonstrates better
understanding of the task. Brief per-case results are appended to
`data/evaluation/question_list_evaluation_brief.csv`; complete questions, randomized label mapping,
and evaluator comments are appended to `data/evaluation/question_list_evaluation_detailed.jsonl`.
The aggregate output reports enriched and baseline wins, ties, and a one-sided exact binomial test
of whether the enriched approach wins more often. Ties are reported and excluded from that test.

## Notes

- Run notebooks only from the repository root, or update the path constants in their configuration cells.
- Do not commit `.env`
- Case text is sent to the configured OpenAI API. Review your organization's privacy and data-handling requirements before using sensitive material.

## Cluster training articles

Open `cluster-train-data.ipynb` and run all cells after installing `requirements.txt`.
It reads existing JSON embeddings from `/data/train/train_index.csv` when present,
otherwise `data/train/train_index.csv`, without making API calls. Article titles come
from Markdown headings in the adjacent `files/` directory, with an ID-based fallback.
The notebook compares DBSCAN and HDBSCAN on L2-normalized embeddings, shows a
neighbor-distance plot for choosing DBSCAN's radius, and visualizes both results
using PCA and t-SNE. Tune the configuration cell and inspect the article examples;
cluster `-1` denotes noise. HDBSCAN is selected for export by default.

Generated files go to the ignored `data/clustering/` directory. At
<https://projector.tensorflow.org/>, use **Load** to select `vectors.tsv` as tensor
and `metadata.tsv` as metadata, then choose `title` for labels and `cluster` for
colors. Vectors contain the original embeddings with no header; metadata contains
article IDs, titles, noise flags, and cluster labels for both algorithms in the
same row order. `clusters.csv` and `run_config.json` support local inspection.
Only visualization is capped at 5,000 articles; clustering and export use all rows.

## Create concise Russian summaries

Run `summarize-train-data.ipynb` from the repository root. It reads the existing
`summary` column from `/data/train/train_index.csv` (or the repository's
`data/train/train_index.csv`), asks ChatGPT for one Russian sentence of at most
35 words without company or product names, and embeds that new description.
It uses `OPENAI_API_KEY` from `.env` and the existing `OPENAI_LLM_MODEL` and
`OPENAI_EMBEDDING_MODEL` settings. API usage incurs charges.

The result is `train_index_summarized.csv` beside the input, with exactly
`id`, `summary`, `embedding` columns; embeddings remain JSON arrays. Each completed
row is saved immediately using an atomic file replacement. Rerunning skips completed
IDs, so an API failure only requires retrying the unfinished row. Set `MAX_NEW_ROWS`
to 5 for an initial style review, then to `None` to finish the index. Review the
resulting descriptions for semantic accuracy and company-name omissions.

A companion `train_index_summarized.state.json` prevents resuming with changed source
summaries, models or prompts. For a different configuration choose a fresh output
path and matching state path, or remove both generated files to rebuild. Run only
one writer per output file. The source index is never overwritten. To cluster the
new descriptions, set `INDEX_PATH` in `cluster-train-data.ipynb` to the new CSV.
