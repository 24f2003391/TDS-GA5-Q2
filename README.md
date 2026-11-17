# TDS GA5 – Q2: Dual Embedding Alignment

A reproducible Python solution for the **Dual Embedding Alignment: Ollama, FAISS, and Rank Correlation** question.

The script embeds the 50 corpus sentences and 10 evaluation queries with two different local Ollama embedding models:

- `nomic-embed-text`
- `mxbai-embed-large`

It builds two independent FAISS inner-product indexes, retrieves the top three documents from each model, computes Spearman's rank correlation across the complete 50-document rankings, validates the result, and writes the final matrix to `answer.json`.

## Repository files

| File | Purpose |
|---|---|
| `dataset.json` | Exact 50-sentence corpus and 10 evaluation queries |
| `solve.py` | Complete embedding, FAISS search, correlation, and validation script |
| `requirements.txt` | Python dependencies |
| `answer.json` | Generated locally when the script runs; not committed |

## 1. Install Ollama

Install Ollama from <https://ollama.com/> and make sure its local server is running.

Pull both required embedding models:

```bash
ollama pull nomic-embed-text
ollama pull mxbai-embed-large
```

You can confirm that both models are installed with:

```bash
ollama list
```

## 2. Set up Python

Python 3.10 or newer is recommended.

Create and activate a virtual environment (optional, but recommended).

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

## 3. Run the solution

Keep `dataset.json` and `solve.py` in the same directory, then run:

```bash
python solve.py
```

The script calls Ollama's batch embedding endpoint:

```
http://localhost:11434/api/embed
```

It sends each model's full list of texts in one request using the `input` field. If Ollama is not running, the models have not been pulled, or the endpoint is unavailable, the script will show the corresponding request error.

## 4. Get the submission matrix

At the end, the script prints the **10 × 7 JSON matrix** in the terminal and saves the same output to:

```
answer.json
```

Open `answer.json` and copy its contents into the assignment submission box.

Each row has this format:

```json
[idx_a1, idx_a2, idx_a3, idx_b1, idx_b2, idx_b3, rho]
```

- The first three indices are the top-3 results from `nomic-embed-text`.
- The next three indices are the top-3 results from `mxbai-embed-large`.
- `rho` is Spearman's rank correlation across all 50 corpus documents, not just the top three.

## Implementation notes

1. Both document and query embeddings are L2-normalized.
2. Since the vectors are normalized, inner product search with `faiss.IndexFlatIP` is equivalent to cosine-similarity search.
3. The script searches all 50 documents for each query. It puts the returned similarity scores back into original document-index order before calculating Spearman's rho.
4. The validation checks the number of rows and columns, valid document indices, distinct top-3 results, valid correlation values, and the assignment's `rho < 0.95` model-diversity condition.

**Important:** The exact numeric output is generated locally by the two embedding models. Do not copy another person's `answer.json` without verifying it against your own run and the assignment's reference tolerance.

## Troubleshooting

- **Connection refused:** Start Ollama and retry.
- **Model not found:** Run both `ollama pull` commands above.
- **Missing Python package:** Activate the intended environment and run `pip install -r requirements.txt`.
- **FAISS installation issue:** Use a supported Python version and install the CPU package listed in `requirements.txt`.

## Disclaimer

This repository is a community solution for learning and reproducing the assignment workflow. Check the assignment instructions and validate your own generated output before submitting.
