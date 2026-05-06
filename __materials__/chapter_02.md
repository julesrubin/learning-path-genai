# Chapter 2: Vertex AI Model Garden

## Context: Expanding StyleCo's AI Capabilities

The customer service assistant impressed stakeholders. Now marketing wants in: StyleCo's catalog has 50,000+ products and writing SEO-friendly descriptions by hand doesn't scale. You'll automate description generation (Gemini) and lifestyle imagery (Imagen).

---

## Learning Resources

**Model Garden** = Google Cloud's catalog of foundation, partner (Anthropic, Cohere), and OSS (Llama, Mistral) models. Browse it in the [Console](https://console.cloud.google.com/vertex-ai/model-garden).

**Gemini family — pick by cost/latency vs. reasoning depth:**
| Model | Use for |
|-------|---------|
| **Gemini 2.5 Pro** | Complex reasoning, deep analysis |
| **Gemini 2.5 Flash** | Balanced — default choice |
| **Gemini 2.5 Flash-Lite** | High volume, lowest latency |

All 1M token context. Multimodal in: text, images, audio, video, PDF.

**Imagen** — text-to-image, editing, inpainting, upscaling. Imagen has 4 variants: `imagen-4.0-generate-001` (standard), `-ultra-` (quality), `-fast-` (speed).

**External references:**
- [Vertex AI Model Garden](https://cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models)
- [Gemini model docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/migrate)
- [Imagen overview](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview)
- [Jinja2 for prompt management](https://medium.com/@alecgg27895/jinja2-prompting-a-guide-on-using-jinja2-templates-for-prompt-management-in-genai-applications-e36e5c1243cf)
- [Structured output with `response_json_schema`](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output)

---

## Your Mission

### 1. Product Description Generator

Create `POST /generate_product_description` returning structured JSON (`description` + `seo_keywords`) for a product.

**Input**: `product_name`, `categories[]`, `materials[]`, `colors[]`, `description_length` (Short/Medium/Long), `target_audience` (Children/Teens/Adults/Seniors/Professionals).

**Implementation:**
- **Models** (`models/product_description.py`) — Pydantic with `Enum` for length & audience.
- **Prompt** — Jinja2 template at `instructions/product_description.j2`.
- **Structured output** — `genai.types.GenerateContentConfig(response_json_schema=...)`, then `ProductDescriptionResponse.model_validate_json(...)`.

### 2. Product Image Generator

Create `POST /generate_product_image` returning base64-encoded images via Imagen.

**Input**: `product_name`, `setting`, `style` (Editorial/Lifestyle/Product-only/Flat-lay), `aspect_ratio` (1:1, 16:9, 9:16, 4:3, 3:4), `image_count` (1–4), `negative_prompt`.

**Implementation:**
- Add `imagen_model_name` and `save_debug_images` to your Pydantic Settings.
- Build prompt by combining product/setting/style; call `client.models.generate_images(...)`; encode bytes → base64.

> [!WARNING]
> **Imagen safety filters return HTTP 200 with empty image bytes** — they don't raise. Always check `generated_image.rai_filtered_reason` *before* accessing `image.image_bytes` and handle with a clean error message if triggered.

Test with deliberately-blocked prompts (political figures, violent imagery) to verify your error path returns a clean 400 instead of crashing.

---

## Bonus Challenges

1. **Multimodal analysis** — `POST /analyze_product_image` accepting an image (base64/URL), using `genai.types.Part.from_image()` to feed it into the description generator.
2. **Prompt enhancement pipeline** — Gemini rewrites a thin user prompt ("silk blouse on model") into a detailed photography brief before passing it to Imagen.

---

## Deploy

Already wired in Chapter 1 — commit + push triggers the build.

---

## Reflection

1. What did Jinja2 templates change about your prompt iteration loop?
2. Where did JSON schema enforcement save you (and where did it get in the way)?
3. Why check `rai_filtered_reason` before `image_bytes`?
4. How would you cap costs at scale on Gemini + Imagen?

---

Next: [Chapter 3: RAG with Vertex AI Search](chapter_03.md) — grounding answers in StyleCo's own data.
