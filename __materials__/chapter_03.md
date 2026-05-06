# Chapter 3: Retrieval-Augmented Generation (RAG)

## Context: Grounding StyleCo's Assistant

Marketing has its image generator. Now the customer service assistant needs to stop hallucinating about return policies, sizing guides, and product specs. Answers must come from **StyleCo's own documents**, not Gemini's training data.

This is **RAG**: retrieve relevant chunks from a knowledge base → stuff them into the prompt → let the model answer with citations.

---

## Learning Resources

**Why RAG over fine-tuning** — cheaper, updatable in seconds, citations are verifiable, no retraining when policies change.

**Core pipeline** (you should be able to draw it):
1. **Ingest** — load documents (PDFs, markdown, JSON catalog)
2. **Chunk** — split into ~200–1000 token segments
3. **Embed** — convert each chunk to a vector (e.g. `text-embedding-005`)
4. **Index** — store vectors in a vector DB
5. **Retrieve** — embed the query, find top-k nearest chunks
6. **Generate** — pass query + retrieved chunks to the LLM

**Three options on GCP — pick by control vs. effort:**

| Option | What it is | When to pick |
|--------|------------|--------------|
| **Vertex AI Search** | Full search product (UI, ranking, faceting, recommendations) | Discovery / search-first UX, retail catalogs |
| **Vertex AI RAG Engine** ⭐ | Managed RAG framework — ingest → chunk → embed → retrieve, with pluggable vector store | Default choice for grounding an LLM |
| **Cloud SQL + pgvector** | Self-managed Postgres with vector extension | When you need full control of chunking, hybrid search, joins with relational data |

**External references:**
- [Vertex AI RAG Engine overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview) — managed RAG
- [RAG Engine quickstart (Python)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-quickstart)
- [Vertex AI Search overview](https://cloud.google.com/generative-ai-app-builder/docs/introduction)
- [pgvector on Cloud SQL](https://cloud.google.com/sql/docs/postgres/extensions#pgvector)
- [Embedding models on Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings)
- ["Lost in the middle" paper](https://arxiv.org/abs/2307.03172) — why chunk order matters

---

## Your Mission

You'll build the StyleCo knowledge assistant on **RAG Engine** (managed path), then explore **pgvector** as a control-heavy alternative.

### 1. Ingest StyleCo Documents into a RAG Corpus

Use the Vertex AI SDK to:
- Create a **RAG corpus** (`vertexai.preview.rag.create_corpus(...)`)
- Import StyleCo product catalog + policy docs from Cloud Storage (`rag.import_files(...)`)
- Configure chunking (chunk size, overlap) and the embedding model

Add `rag_corpus_name` to your Pydantic Settings.

### 2. Grounded Q&A Endpoint

Create `POST /styleco_rag` accepting a customer question and returning:
```json
{
  "answer": "...",
  "citations": [
    {"source": "policies/returns.md", "snippet": "..."}
  ]
}
```

**Implementation:**
- Retrieve with `rag.retrieval_query(...)` to get top-k chunks
- Pass chunks as context to Gemini via `Tool.from_retrieval(...)` (native grounding)
- Return both the answer and the source citations — non-negotiable for trust

> [!IMPORTANT]
> **Always surface citations.** A grounded answer without sources is indistinguishable from a hallucination to the user.

### 3. Evaluate

Hand-write 10 sample customer questions covering: clear hits (policy docs), edge cases (info not in corpus), and ambiguous queries. For each, check:
- Did retrieval return the right chunks?
- Did the model stick to retrieved context, or invent?
- Are citations correct?

Document failures — they drive your chunk-size / top-k tuning.

---

## Bonus: Cloud SQL + pgvector Alternative

For comparison, implement the **same Q&A endpoint** against a self-managed pipeline:

- Provision Cloud SQL Postgres with the `pgvector` extension (Terraform in `iac/`)
- Write your own ingestion: read docs → chunk → embed (`text-embedding-005`) → `INSERT` rows with a `vector(768)` column
- Retrieve via `ORDER BY embedding <=> query_embedding LIMIT k` (cosine distance)
- Build the same response shape

**Then write a short comparison** (`claudedocs/rag-comparison.md`) — managed RAG Engine vs. pgvector on:
- Lines of code to ship
- Cost at 10K queries/month
- Control over chunking & retrieval
- Operational burden (backups, scaling, schema migrations)

---

## Reflection

1. What chunk size worked best for StyleCo's policy docs vs. product catalog? Why?
2. When would you reach for Vertex AI Search instead of RAG Engine?
3. How would you handle a question whose answer is split across 3 documents?
4. What's your strategy when retrieval returns nothing relevant — refuse, fall back to general Gemini, or ask a clarifying question?

---

Next: [Chapter 4: Function Calling](chapter_04.md) — letting the assistant *act* (check stock, look up orders), not just *answer*.
