# TDS GA5 – Q2: Dual Embedding Alignment

A reproducible Python solution for the **Dual Embedding Alignment: Ollama, FAISS, and Rank Correlation** question.

The program embeds a corpus and its evaluation queries with two local Ollama embedding models:

- `nomic-embed-text`
- `mxbai-embed-large`

It builds separate FAISS inner-product indexes, retrieves the top three documents from each model, calculates Spearman's rank correlation over the complete document rankings, and writes a JSON result matrix.

> **Important:** The repository's `dataset.json` is the assignment dataset used when this solution was prepared. If your assignment portal gives you a different dataset, use your own downloaded JSON file as described below. Do not assume that another student's dataset or output is interchangeable with yours.

## Repository files

| File | Purpose |
|---|---|
| `dataset.json` | Included assignment dataset (50 sentences and 10 queries) |
| `solve.py` | Embedding, FAISS search, correlation, and validation |
| `requirements.txt` | Python dependencies |
| `answer.json` | Generated locally when the script runs; not committed |
| `custom_dataset.example.json` | Example structure for your own corpus and queries |

## 1. Install Ollama and the embedding models

Install Ollama from <https://ollama.com/> and make sure its local server is running.

Pull both models:

```bash
ollama pull nomic-embed-text
ollama pull mxbai-embed-large
```

Confirm they are installed:

```bash
ollama list
```

## 2. Set up Python

Python 3.10 or newer is recommended. A virtual environment is optional but recommended.

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Linux / macOS / WSL

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Use your own JSON dataset

You do **not** need to edit `solve.py`. Create a JSON file containing:

- A non-empty `sentences` array (or, alternatively, a `documents` array).
- A non-empty `queries` array.
- Every array item must be a non-empty string.
- At least three documents are needed because the program returns a top-3 ranking for each query.

Example:

```json
{
  "documents": [
    "A document about database indexing.",
    "A document about distributed systems.",
    "A document about machine learning."
  ],
  "queries": [
    "How do database indexes work?",
    "What is distributed consensus?"
  ]
}
```

You can also use the assignment's original `sentences` key instead of `documents`:

```json
{
  "sentences": [
    "First corpus sentence.",
    "Second corpus sentence.",
    "Third corpus sentence."
  ],
  "queries": [
    "First question?",
    "Second question?"
  ]
}
```

### Steps

1. Download your own dataset JSON from the assignment portal.
2. Put it in the same folder as `solve.py` (or note its full path).
3. Make sure its structure matches one of the examples above. If it has different key names or nested objects, convert it to this structure first.
4. Run the script with the path to your file:

```powershell
python solve.py --input .\my_dataset.json --output .\my_answer.json
```

On Linux/macOS/WSL, the equivalent is:

```bash
python solve.py --input ./my_dataset.json --output ./my_answer.json
```

If you name your file `dataset.json` and put it beside `solve.py`, you can simply run `python solve.py`.

The script accepts any positive number of queries and three or more documents; it creates one output row per query. However, **the assignment grader may require fixed dimensions** (for this GA5 question, 50 documents and 10 queries). For a graded submission, use the exact dataset and dimensions required by your own assignment page.

## 4. Run with the default assignment dataset

If you want to use the dataset included in this repository:

```bash
python solve.py
```

The script calls Ollama's batch embedding endpoint:

```
http://localhost:11434/api/embed
```

If Ollama is hosted somewhere else, provide its base URL:

```bash
python solve.py --ollama-url http://localhost:11434
```

You can also choose different installed embedding models:

```bash
python solve.py --model-a nomic-embed-text --model-b mxbai-embed-large
```

The model names can also be set with the `MODEL_A` and `MODEL_B` environment variables, and the server URL with `OLLAMA_URL`.

## 5. Understand the output

The output contains one row for each query:

```json
[idx_a1, idx_a2, idx_a3, idx_b1, idx_b2, idx_b3, rho]
```

- The first three indices are the top-3 document results from model A.
- The next three indices are the top-3 document results from model B.
- `rho` is Spearman's rank correlation across **all documents**, not just the top three.
- Document indices are zero-based, so the first document is index `0`.

By default, the result is printed in the terminal and saved to `answer.json`. If you pass `--output my_answer.json`, it is saved to that path instead. Copy the generated matrix into the assignment submission field only after checking that you used the correct dataset.

## Implementation notes

1. Document and query embeddings are L2-normalized.
2. With normalized vectors, inner-product search using `faiss.IndexFlatIP` is equivalent to cosine-similarity search.
3. Each model has its own index. The script searches every document and restores similarity scores to original document order before calculating Spearman's rho.
4. The script checks input structure, embedding response shapes, finite values, top-3 indices, and correlation values.
5. The script deliberately does not hard-code 50 documents or 10 queries, so it can also be reused with other datasets. The assignment's own grader can still enforce its required dimensions and thresholds.

## Troubleshooting

- **Connection refused:** Start Ollama and retry.
- **Model not found:** Run the two `ollama pull` commands.
- **Input file not found:** Check the path supplied to `--input`.
- **Invalid JSON / missing keys:** Check that the file is valid JSON and contains `sentences` or `documents`, plus `queries`.
- **Missing Python package:** Activate the intended environment and run `pip install -r requirements.txt`.
- **FAISS installation issue:** Use a supported Python version and install the CPU package listed in `requirements.txt`.

## Disclaimer

This repository is a community solution for learning and reproducing the workflow. Check your assignment's exact instructions and validate your own generated output before submitting.
