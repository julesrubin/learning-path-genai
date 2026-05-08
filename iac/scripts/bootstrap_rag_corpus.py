# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "google-cloud-aiplatform>=1.119.0",
# ]
# ///
"""
Bootstrap a Vertex AI RAG Engine corpus for StyleCo.

Idempotent:
  - If a corpus with display_name == RAG_CORPUS_DISPLAY_NAME exists, reuse it.
  - Otherwise create one with the configured embedding model.
  - Re-import files from the GCS bucket on every run (RAG Engine deduplicates by URI).

This script is the manual step that Terraform can't do today: the provider has
no resource for `google_vertex_ai_rag_corpus` or `google_vertex_ai_rag_file`.
Run it once after `terraform apply`, and again whenever you push new docs to
the bucket.

Usage:
  cd iac
  uv run scripts/bootstrap_rag_corpus.py gs://<bucket-name>

Env vars (with defaults):
  GOOGLE_CLOUD_PROJECT      (required)
  GOOGLE_CLOUD_LOCATION     europe-west1
  RAG_CORPUS_DISPLAY_NAME   styleco-knowledge-base
  RAG_EMBEDDING_MODEL       publishers/google/models/text-embedding-005
  RAG_CHUNK_SIZE            512
  RAG_CHUNK_OVERLAP         100
"""

from __future__ import annotations

import os
import sys

import vertexai
from vertexai import rag


def _env(name: str, default: str | None = None) -> str:
    value = os.environ.get(name, default)
    if value is None:
        sys.exit(f"ERROR: env var {name} is required")
    return value


def bootstrap(gcs_uri: str) -> str:
    project = _env("GOOGLE_CLOUD_PROJECT")
    location = _env("GOOGLE_CLOUD_LOCATION", "europe-west1")
    display_name = _env("RAG_CORPUS_DISPLAY_NAME", "styleco-knowledge-base")
    embedding_model = _env(
        "RAG_EMBEDDING_MODEL", "publishers/google/models/text-embedding-005"
    )
    chunk_size = int(_env("RAG_CHUNK_SIZE", "512"))
    chunk_overlap = int(_env("RAG_CHUNK_OVERLAP", "100"))

    vertexai.init(project=project, location=location)

    corpus = next(
        (c for c in rag.list_corpora() if c.display_name == display_name),
        None,
    )

    if corpus is None:
        print(f"Creating corpus '{display_name}'...")
        corpus = rag.create_corpus(
            display_name=display_name,
            backend_config=rag.RagVectorDbConfig(
                rag_embedding_model_config=rag.RagEmbeddingModelConfig(
                    vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                        publisher_model=embedding_model,
                    ),
                ),
            ),
        )
        print(f"Created: {corpus.name}")
    else:
        print(f"Reusing existing corpus: {corpus.name}")

    print(f"Importing files from {gcs_uri}...")
    response = rag.import_files(
        corpus.name,
        [gcs_uri],
        transformation_config=rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(
                chunk_size=chunk_size, chunk_overlap=chunk_overlap
            ),
        ),
    )
    print(
        f"Imported {response.imported_rag_files_count} files "
        f"(skipped: {response.skipped_rag_files_count}, "
        f"failed: {response.failed_rag_files_count})"
    )

    return corpus.name


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].startswith("gs://"):
        print("Usage: bootstrap_rag_corpus.py gs://<bucket-name>", file=sys.stderr)
        sys.exit(1)

    corpus_name = bootstrap(sys.argv[1])
    print(f"\nCorpus ready: {corpus_name}")
