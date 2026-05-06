# Chapter 1: LLM Fundamentals

## Context: Meet StyleCo

You've joined a team building an AI-powered Customer Experience Platform for **StyleCo**, a European fashion retailer (200+ stores, 12 countries). Their support team handles thousands of daily inquiries — product, sizing, orders, recommendations, returns — currently via phone, email, and basic chatbots that frustrate customers.

Over the coming chapters, you'll progressively build the GenAI stack: API calls → RAG → function calling → MCP → full agents. This chapter is your foundation: understand the basics, ship your first endpoints.

---

## Learning Resources

Skim these before coding. Don't go down rabbit holes — practical work below is what matters.

**Core concepts (keywords to know):**
- **Tokens / tokenization** — subword units; drive cost, latency, context limits, play with [Gemini tokenizer playground](https://ai.google.dev/gemini-api/docs/tokens)
- **Embeddings** — vectors capturing meaning; foundation for RAG (Chapters 4–5)
- **Context window** — total tokens per request (Gemini 2.5 Flash: 1M); beware ["lost in the middle"](https://arxiv.org/abs/2307.03172)
- **Attention** — quadratic cost in sequence length; explains why context windows are bounded
- **Generation params** — `temperature` (0 deterministic → 1+ creative), `top_p`, `top_k`, `max_tokens`
- **Limitations** — hallucinations, knowledge cutoff, no real-time data, prompt injection

**Prompting techniques** (you'll use all three):
| Technique | When to use |
|-----------|-------------|
| **Zero-shot** | Simple, well-defined tasks |
| **Few-shot** | When format/style matters — show 2–5 examples |
| **Chain-of-thought** | Complex reasoning, multi-step analysis |

**External references** (read what's relevant to your task):
- [FT Generative AI Explainer](https://ig.ft.com/generative-ai/) — visual deep-dive
- [Google Gen AI SDK](https://cloud.google.com/vertex-ai/generative-ai/docs/sdks/overview) + [Python SDK reference](https://googleapis.github.io/python-genai/)
- [Prompt Design Strategies](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies)
- [Prompt Engineering Whitepaper](https://www.kaggle.com/whitepaper-prompt-engineering)
- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)

---

## Project Structure

Work inside `cloud_run/genai-api/`:

```
cloud_run/genai-api/
├── main.py              # FastAPI entrypoint
├── instructions/        # System prompts (externalized)
├── models/              # Pydantic request/response schemas
├── services/            # Gemini calls + business logic
├── routers/             # Your endpoints
├── pyproject.toml
└── Dockerfile
```

**Configuration**: use **Pydantic Settings** (loads `.env` + env vars, validates at startup). Never call `os.getenv()` in services — always go through the `settings` object so the app fails fast on missing config.

---

## Your Mission

### 1. Hello, Gemini
Create `POST /hello_gemini` accepting `{"prompt": "..."}` and returning `{"response": "..."}`. Use the [Google Gen AI SDK](https://cloud.google.com/vertex-ai/generative-ai/docs/sdks/overview).

### 2. StyleCo Customer Service
Create `POST /styleco_assistant` powered by a system prompt loaded from `instructions/styleco_customer_service.txt`. The prompt should make the assistant: professional + friendly, fashion/retail savvy, honest about unknowns, polite when declining competitor questions.

> [!WARNING]
> Never hardcode system prompts in code. Externalize to files for iteration and version control.

### 3. Temperature Experiments
Create `POST /styleco_assistant_temperature` accepting a message and `temperatures: list[float]` (default `[0.0, 0.5, 1.0]`). Return one response per temperature so you can compare behaviors.

### 4. Token Analysis Utility
Add a `token_analysis(prompt: str) -> dict` method to your `GeminiClient` returning `token_count`, `estimated_cost_usd`, `context_usage_percent`, `warnings`. **Bonus**: expose via `POST /token_analysis`.

### 5. Deploy to Cloud Run
Add `genai-api` to `_SERVICES_TO_BUILD` in `cloudbuild.yaml` and push. Cloud Build handles image push + Terraform deploy.

> [!TIP]
> Cloud Run service isn't publicly exposed. Test via:
> ```bash
> gcloud run services proxy genai-api --region=europe-west1
> ```

---

## Reflection

1. How do token limits constrain a long customer-service conversation?
2. Which prompting technique fits product recommendations best?
3. How could hallucinations damage customer trust — and how would you mitigate?
4. Factual vs. creative queries — what temperature for each?

---

Next: [Chapter 2: Vertex AI Model Garden](chapter_02.md) — picking the right Gemini model per use case.
