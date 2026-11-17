#!/usr/bin/env python3
"""Compare two Ollama embedding models on a JSON corpus using FAISS and Spearman rho."""

import argparse
import json
import os
import sys
from pathlib import Path

import faiss
import numpy as np
import requests
from scipy.stats import spearmanr

DEFAULT_INPUT = "dataset.json"
DEFAULT_OUTPUT = "answer.json"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL_A = "nomic-embed-text"
DEFAULT_MODEL_B = "mxbai-embed-large"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare two Ollama embedding models on documents and queries."
    )
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Input JSON file (default: dataset.json)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output JSON file (default: answer.json)")
    parser.add_argument("--model-a", default=os.getenv("MODEL_A", DEFAULT_MODEL_A))
    parser.add_argument("--model-b", default=os.getenv("MODEL_B", DEFAULT_MODEL_B))
    parser.add_argument("--ollama-url", default=os.getenv("OLLAMA_URL", DEFAULT_OLLAMA_URL),
                        help="Ollama server base URL (default: http://localhost:11434)")
    return parser.parse_args()


def load_dataset(path):
    """Load documents/sentences and queries from a JSON object."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Input file not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("The JSON root must be an object.")

    # Accept both the assignment's original key and the more general alias.
    documents = data.get("sentences", data.get("documents"))
    queries = data.get("queries")

    if not isinstance(documents, list) or not documents:
        raise ValueError('JSON must contain a non-empty "sentences" or "documents" array.')
    if len(documents) < 3:
        raise ValueError("At least 3 documents are required to return a top-3 ranking.")
    if not isinstance(queries, list) or not queries:
        raise ValueError('JSON must contain a non-empty "queries" array.')

    for field, values in (("documents/sentences", documents), ("queries", queries)):
        if any(not isinstance(value, str) or not value.strip() for value in values):
            raise ValueError(f'Every item in "{field}" must be a non-empty string.')

    return documents, queries


def get_embeddings(model_name, texts, ollama_url):
    """Embed a batch of texts with Ollama and return normalized float32 vectors."""
    endpoint = f"{ollama_url.rstrip('/')}/api/embed"
    try:
        response = requests.post(
            endpoint,
            json={"model": model_name, "input": texts},
            timeout=600,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Could not get embeddings from {endpoint} using {model_name}: {exc}\n"
            "Check that Ollama is running and that the model has been pulled."
        ) from exc

    try:
        payload = response.json()
        embeddings = np.asarray(payload["embeddings"], dtype=np.float32)
    except (ValueError, KeyError, TypeError) as exc:
        raise RuntimeError(f"Unexpected embedding response from model {model_name}.") from exc

    if embeddings.ndim != 2 or embeddings.shape[0] != len(texts):
        raise RuntimeError(
            f"{model_name} returned shape {embeddings.shape}; "
            f"expected {len(texts)} embedding vectors."
        )
    if embeddings.shape[1] == 0 or not np.isfinite(embeddings).all():
        raise RuntimeError(f"{model_name} returned empty or non-finite embedding values.")

    faiss.normalize_L2(embeddings)
    return embeddings


def build_index(embeddings):
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    return index


def main():
    args = parse_args()
    documents, queries = load_dataset(args.input)

    print(f"Loaded {len(documents)} documents and {len(queries)} queries.")
    print(f"Model A: {args.model_a}")
    print(f"Model B: {args.model_b}")

    print("\nEmbedding documents with model A...")
    docs_a = get_embeddings(args.model_a, documents, args.ollama_url)
    print("Embedding documents with model B...")
    docs_b = get_embeddings(args.model_b, documents, args.ollama_url)

    if docs_a.shape[1] != docs_b.shape[1]:
        print(
            "Note: the models use different vector dimensions "
            f"({docs_a.shape[1]} and {docs_b.shape[1]}). "
            "This is fine because each model has its own FAISS index."
        )

    index_a = build_index(docs_a)
    index_b = build_index(docs_b)

    print("\nEmbedding queries with model A...")
    query_a = get_embeddings(args.model_a, queries, args.ollama_url)
    print("Embedding queries with model B...")
    query_b = get_embeddings(args.model_b, queries, args.ollama_url)

    if query_a.shape[1] != docs_a.shape[1]:
        raise RuntimeError(f"{args.model_a} returned different dimensions for documents and queries.")
    if query_b.shape[1] != docs_b.shape[1]:
        raise RuntimeError(f"{args.model_b} returned different dimensions for documents and queries.")

    matrix = []
    for query_number in range(len(queries)):
        print(f"Searching query {query_number + 1}/{len(queries)}...")
        distances_a, indices_a = index_a.search(query_a[query_number:query_number + 1], len(documents))
        distances_b, indices_b = index_b.search(query_b[query_number:query_number + 1], len(documents))

        top3_a = indices_a[0][:3].astype(int).tolist()
        top3_b = indices_b[0][:3].astype(int).tolist()

        # Restore scores to original document order before comparing rankings.
        scores_a = np.empty(len(documents), dtype=np.float64)
        scores_b = np.empty(len(documents), dtype=np.float64)
        scores_a[indices_a[0]] = distances_a[0]
        scores_b[indices_b[0]] = distances_b[0]

        rho = float(spearmanr(scores_a, scores_b).statistic)
        if not np.isfinite(rho):
            raise RuntimeError(
                f"Spearman correlation was undefined for query {query_number + 1}."
            )

        matrix.append(top3_a + top3_b + [round(rho, 4)])

    # Structural checks. The assignment-specific grader may impose additional
    # dimensions or thresholds; this script does not assume every user's file
    # has exactly 50 documents and 10 queries.
    if len(matrix) != len(queries) or any(len(row) != 7 for row in matrix):
        raise RuntimeError("Internal error: output matrix has an unexpected shape.")

    for number, row in enumerate(matrix, start=1):
        if any(not isinstance(i, int) or not 0 <= i < len(documents) for i in row[:6]):
            raise RuntimeError(f"Invalid document index in output row {number}.")
        if len(set(row[:3])) != 3 or len(set(row[3:6])) != 3:
            raise RuntimeError(f"Duplicate top-3 document index in output row {number}.")
        if not np.isfinite(row[6]) or not -1 <= row[6] <= 1:
            raise RuntimeError(f"Invalid Spearman rho in output row {number}.")

    output_path = Path(args.output)
    output_path.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")

    print("\nFinal result:")
    print(json.dumps(matrix, indent=2))
    print(f"\nSaved {len(matrix)} rows to: {output_path.resolve()}")
    print("For the GA5 assignment, check that your input is the official dataset and")
    print("that the output dimensions and rho values satisfy the grader's requirements.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError) as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        sys.exit(1)
