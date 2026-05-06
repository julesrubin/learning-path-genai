# Chapter 3: Retrieval-Augmented Generation (RAG)

## Context: Grounding StyleCo's Assistant

The customer service assistant must stop hallucinating about return policies, sizing guides, and product specs. Answers must come from **StyleCo's own documents**, not Gemini's training data.

**RAG** in one line: retrieve relevant chunks from a knowledge base → inject into the prompt → model answers with citations.

---

## Learning Resources

**Three options on GCP — pick by control vs. effort:**

| Option | When to pick |
|--------|--------------|
| **Vertex AI Search** | Discovery / search-first UX, retail catalogs |
| **Vertex AI RAG Engine** ⭐ | Default for grounding an LLM (managed, pluggable vector store) |
| **Cloud SQL + pgvector** | Full control of chunking, hybrid search, joins with relational data |

**External references:**
- [RAG Engine overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview) + [Python quickstart](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-quickstart)
- [Vertex AI Search](https://cloud.google.com/generative-ai-app-builder/docs/introduction)
- [pgvector on Cloud SQL](https://cloud.google.com/sql/docs/postgres/extensions#pgvector)
- [Embedding models](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings) · ["Lost in the middle"](https://arxiv.org/abs/2307.03172)
- [RAG Engine + Terraform walkthrough](https://dev.to/suhas_mallesh/vertex-ai-rag-engine-with-terraform-your-first-rag-pipeline-on-gcp-1gfi)

---

## Your Mission

Build the StyleCo knowledge assistant on **RAG Engine**, then explore **pgvector** as a control-heavy alternative.

### 1. Provision Infrastructure (Terraform)

Terraform covers the *infra* of RAG Engine but **not corpus or file resources** — those live in the Python SDK. In `iac/`:

- `google_storage_bucket` — source docs
- `google_service_account` + `google_project_iam_member` (`roles/aiplatform.user`) + bucket IAM for the Vertex AI Service Agent
- `google_vertex_ai_rag_engine_config` — project tier (`basic` → `scaled` for prod)
- `google_project_service` — enable `aiplatform.googleapis.com`, `storage.googleapis.com`

### 2. Bootstrap Corpus + Ingest (Python)

A small idempotent script, runnable on first deploy and re-runnable safely:

- `rag.list_corpora()` → reuse if present, else `rag.create_corpus(...)` with chunking + embedding model (`text-embedding-005`)
- `rag.import_files(...)` from the GCS bucket
- Surface the corpus resource ID via Pydantic Settings (or look it up at startup)

### 3. Grounded Q&A Endpoint

Create `POST /styleco_rag` returning `answer` + `citations[]` (each with `source` + `snippet`).

- Retrieve via `rag.retrieval_query(...)`
- Ground Gemini with `Tool.from_retrieval(...)`
- Always surface citations — without sources, a grounded answer is indistinguishable from a hallucination

### 4. Evaluate

Hand-write 10 sample questions: clear hits, edge cases (info absent), ambiguous queries. For each, check retrieval relevance, model faithfulness to context, and citation correctness. Failures drive your chunk-size / top-k tuning.

---

## Bonus: Cloud SQL + pgvector

Implement the same endpoint against a self-managed pipeline (Cloud SQL Postgres + `pgvector`, custom chunking + embedding, retrieve via `ORDER BY embedding <=> query_embedding LIMIT k`).

Write a short comparison (`claudedocs/rag-comparison.md`) on lines of code, cost at 10K queries/month, control, and ops burden.

---

## Reflection

1. Best chunk size for policy docs vs. product catalog — why?
2. When Vertex AI Search instead of RAG Engine?
3. Strategy when retrieval returns nothing relevant — refuse, fall back, clarify?

---

Next: [Chapter 4: Function Calling](chapter_04.md) — letting the assistant *act*, not just *answer*.
