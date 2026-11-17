import json
from pathlib import Path

import faiss
import numpy as np
import requests
from scipy.stats import spearmanr

# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATASET_PATH = Path("dataset.json")
OUTPUT_PATH = Path("answer.json")
OLLAMA_URL = "http://localhost:11434/api/embed"

MODEL_A = "nomic-embed-text"
MODEL_B = "mxbai-embed-large"


# --------------------------------------------------
# 1. LOAD DATASET
# --------------------------------------------------

with DATASET_PATH.open("r", encoding="utf-8") as f:
    data = json.load(f)

sentences = data["sentences"]
queries = data["queries"]

print("Sentences:", len(sentences))
print("Queries:", len(queries))

assert len(sentences) == 50, "Expected exactly 50 corpus sentences."
assert len(queries) == 10, "Expected exactly 10 evaluation queries."


# --------------------------------------------------
# 2. GENERATE AND NORMALIZE EMBEDDINGS
# --------------------------------------------------

def get_embeddings(model_name, texts):
    """Embed a list of texts using Ollama's /api/embed endpoint."""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model_name,
            "input": texts,
        },
        timeout=300,
    )
    response.raise_for_status()

    result = response.json()
    embeddings = np.asarray(result["embeddings"], dtype=np.float32)

    if embeddings.ndim != 2 or len(embeddings) != len(texts):
        raise ValueError(
            f"Unexpected embedding shape from {model_name}: {embeddings.shape}"
        )

    if not np.isfinite(embeddings).all():
        raise ValueError(f"{model_name} returned non-finite embedding values.")

    # Normalize every vector to unit length. Inner product then equals cosine
    # similarity (apart from floating-point precision).
    faiss.normalize_L2(embeddings)
    return embeddings


# --------------------------------------------------
# 3. EMBED THE CORPUS WITH BOTH MODELS
# --------------------------------------------------

print("\nGenerating Nomic document embeddings...")
emb_a = get_embeddings(MODEL_A, sentences)
print("Nomic embeddings:", emb_a.shape)

print("\nGenerating Mxbai document embeddings...")
emb_b = get_embeddings(MODEL_B, sentences)
print("Mxbai embeddings:", emb_b.shape)


# --------------------------------------------------
# 4. BUILD TWO INDEPENDENT FAISS INDEXES
# --------------------------------------------------

index_a = faiss.IndexFlatIP(emb_a.shape[1])
index_a.add(emb_a)

index_b = faiss.IndexFlatIP(emb_b.shape[1])
index_b.add(emb_b)

print("\nFAISS indexes created successfully.")


# --------------------------------------------------
# 5. EMBED ALL EVALUATION QUERIES
# --------------------------------------------------

print("\nGenerating query embeddings...")
query_a = get_embeddings(MODEL_A, queries)
query_b = get_embeddings(MODEL_B, queries)


# --------------------------------------------------
# 6. SEARCH AND CALCULATE SPEARMAN'S RHO
# --------------------------------------------------

matrix = []

for q in range(len(queries)):
    print(f"\nProcessing query {q + 1}/{len(queries)}")

    # Search all 50 corpus documents so correlation uses the full ranking.
    distances_a, indices_a = index_a.search(query_a[q:q + 1], len(sentences))
    distances_b, indices_b = index_b.search(query_b[q:q + 1], len(sentences))

    top3_a = indices_a[0][:3].tolist()
    top3_b = indices_b[0][:3].tolist()

    # Put similarity scores back into original corpus order (document 0..49).
    scores_a = np.zeros(len(sentences), dtype=np.float64)
    scores_b = np.zeros(len(sentences), dtype=np.float64)

    scores_a[indices_a[0]] = distances_a[0]
    scores_b[indices_b[0]] = distances_b[0]

    # Spearman correlation compares the two complete 50-document rankings.
    rho, _ = spearmanr(scores_a, scores_b)
    rho = round(float(rho), 4)

    row = [
        int(top3_a[0]), int(top3_a[1]), int(top3_a[2]),
        int(top3_b[0]), int(top3_b[1]), int(top3_b[2]),
        rho,
    ]
    matrix.append(row)


# --------------------------------------------------
# 7. VALIDATE THE SUBMISSION MATRIX
# --------------------------------------------------

assert len(matrix) == 10, "Output must contain 10 rows."

for row_number, row in enumerate(matrix, start=1):
    assert len(row) == 7, f"Row {row_number} must contain 7 values."

    indices = row[:6]
    assert all(
        isinstance(i, int) and 0 <= i < 50 for i in indices
    ), f"Invalid document index in row {row_number}."

    assert len(set(row[:3])) == 3, f"Model A top-3 has duplicates in row {row_number}."
    assert len(set(row[3:6])) == 3, f"Model B top-3 has duplicates in row {row_number}."

    assert np.isfinite(row[6]) and -1.0 <= row[6] <= 1.0
    assert row[6] < 0.95, (
        f"Correlation in row {row_number} is >= 0.95. "
        "Check that two different embedding models were used."
    )


# --------------------------------------------------
# 8. PRINT AND SAVE THE FINAL JSON
# --------------------------------------------------

output = json.dumps(matrix, indent=2)

print("\n" + "=" * 60)
print("FINAL 10 x 7 SUBMISSION MATRIX")
print("=" * 60)
print(output)

OUTPUT_PATH.write_text(output + "\n", encoding="utf-8")
print(f"\nSaved successfully to {OUTPUT_PATH}")
