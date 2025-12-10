# Chapter 1: LLM Fundamentals

## Context: Meet StyleCo

Welcome to your mission! You've just joined a project team working with **StyleCo**, a European fashion retailer with 200+ stores across 12 countries. They're embarking on an ambitious digital transformation: building an AI-powered Customer Experience Platform.

### The Business Challenge

StyleCo's customer service team handles thousands of inquiries daily:
- Product availability and sizing questions
- Order status and shipping updates
- Style recommendations and outfit suggestions
- Returns and exchange requests
- Store location and hours

Currently, these are handled by a mix of phone support, email, and basic chatbots that frustrate customers with canned responses. StyleCo wants to revolutionize this with GenAI.

### Your Role

Over the coming weeks, you'll build progressively sophisticated AI solutions:
1. **This chapter**: Understand how LLMs work and make your first API calls
2. **Later chapters**: Build RAG systems, function calling, MCP servers, and full AI agents

But first, you need to understand the technology you're working with.

---

## Learning Resources

### How LLMs Work

Before writing any code, invest time understanding the fundamentals. Large Language Models are built on **transformer architecture** using self-attention mechanisms to process and generate text. Understanding these core concepts will help you make better decisions when building AI applications.

> [!TIP]
> For an interactive visual exploration of how generative AI works, check out the [Financial Times' Generative AI Explainer](https://ig.ft.com/generative-ai/) - it provides excellent visualizations of the technology behind LLMs.

#### Tokens and Tokenization

LLMs don't see text the way humans do - they process **tokens**, which are subword units that form the basic building blocks of language understanding:

**How Tokenization Works:**
- The word "tokenization" might become `["token", "ization"]`
- Common words are often single tokens: "the", "is", "cat"
- Rare or compound words are split: "uncommon" → `["un", "common"]`
- Numbers and special characters have their own tokenization rules
- **Multilingual impact**: Non-Latin scripts (Chinese, Arabic, Russian) typically require more tokens per word, affecting costs

**Why Tokens Matter:**
- **Cost**: Most LLM APIs charge per token (input + output)
- **Context limits**: Models have maximum token counts (e.g., 1M tokens for Gemini)
- **Performance**: More tokens = longer processing time
- **Quality**: Token boundaries can affect model understanding of rare words or specialized terminology

**Real-world example**:
- English: "Hello, how are you?" = ~6 tokens
- French: "Bonjour, comment allez-vous?" = ~8 tokens
- Japanese: "こんにちは、お元気ですか？" = ~15+ tokens

> [!TIP]
> Use the [Gemini tokenizer playground](https://ai.google.dev/gemini-api/docs/tokens) to see how your text gets tokenized. This is essential for estimating costs and understanding context usage.

#### Embeddings and Vector Space

Text is converted to high-dimensional vectors called **embeddings** - numerical representations that capture semantic meaning:

**Core Concepts:**
- **Dimensionality**: Embeddings typically have 768 to 3072 dimensions (think of it as coordinates in a 768-dimensional space)
- **Semantic similarity**: Words with similar meanings cluster together in vector space
  - "king" and "monarch" have vectors close to each other
  - "king" and "bicycle" have vectors far apart
- **Mathematical operations**: You can do arithmetic with embeddings
  - `king - man + woman ≈ queen`

> [!TIP]
> See [this article](https://medium.com/@manansuri/a-dummys-guide-to-word2vec-456444f3c673) for an accessible introduction to word embeddings and how they capture meaning.

**Practical Applications:**
- **Semantic search**: Find documents by meaning, not just keywords
  - Query: "how to fix water damage" matches "repairing flood issues"
- **Recommendation systems**: Find similar products or content
- **Clustering**: Group similar customer inquiries automatically
- **RAG (Retrieval-Augmented Generation)**: Core technology for Chapters 4-5
  - Store document embeddings in vector databases
  - Retrieve relevant context based on query similarity

**Distance Metrics:**
- **Cosine similarity**: Measures angle between vectors (most common)
- **Euclidean distance**: Straight-line distance in vector space
- **Dot product**: Fast approximation for normalized vectors

> [!NOTE]
> Embeddings are why StyleCo can implement semantic search for their product catalog - customers can search "summer dress for beach wedding" and find relevant products even if those exact words don't appear in product descriptions.

#### Context Windows

The context window is the "memory" of a conversation - the total amount of text (in tokens) a model can process in a single request:

**Current Capabilities:**
- **Gemini 2.5 Flash**: up to 1M tokens (~750,000 words or ~1,500 pages)
- **GPT-5.1**: up to 400K tokens
- **Claude Opus 4.5**: up to 200K tokens

**Context Window Economics:**
- **Larger context = higher cost**: Processing 1M tokens costs significantly more than 10K
- **Latency impact**: More tokens to process = slower response times
- **Quality degradation**: Models may struggle to maintain coherence across very long contexts (see ["lost in the middle" problem](https://arxiv.org/abs/2307.03172))

**What Happens When You Exceed Context:**
- Request fails with error (hard limit)
- Need to truncate or summarize earlier messages
- Implement sliding window approach (keep recent context, drop old)

**Strategic Context Management:**
- **Conversation summarization**: Periodically compress chat history
- **Selective context**: Only include relevant parts of long documents
- **Context caching**: Reuse common context across requests
- **Chunking strategies**: Break large documents into manageable pieces

> [!IMPORTANT]
> For StyleCo's customer service, context management is crucial. A customer with a 20-message conversation history will consume significant tokens. You'll learn techniques for efficient context management throughout the learning path, including conversation summarization, semantic chunking, and context compression.

#### The Attention Mechanism

While you don't need to understand the math, knowing about **attention** helps you understand LLM behavior:

- **Self-attention**: The model learns which words in the input are relevant to each other
- **Multi-head attention**: Multiple attention mechanisms run in parallel, capturing different relationships
- **Why it matters**:
  - Models can handle long-range dependencies ("the animal ... it" even with 100 words between)
  - Attention patterns reveal what the model "focuses on" when generating responses
  - Computational cost grows quadratically with sequence length (why context windows have limits)

### Prompting Techniques

Prompting is the primary way you "program" LLMs. Different techniques work better for different tasks:

| Technique | Description | When to Use | Example |
|-----------|-------------|-------------|---------|
| **Zero-shot** | Direct instructions without examples | Simple, well-defined tasks with clear objectives | "Translate this to French: Hello" |
| **Few-shot** | Include 2-5 example input/output pairs | When format, style, or structure matters; teaching pattern recognition | "Classify sentiment:\nReview: Great product! → Positive\nReview: Terrible quality. → Negative\nReview: It's okay. → ?" |
| **Chain-of-thought (CoT)** | Instruct model to show reasoning steps before answering | Complex reasoning, math problems, multi-step analysis | "Let's solve this step by step:\n1. First identify...\n2. Then calculate...\n3. Finally conclude..." |

**Advanced Prompting Patterns:**

1. **System/User/Assistant structure**:
   ```
   System: You are a helpful assistant specializing in [domain]
   User: [user's question]
   Assistant: [model's response]
   ```

2. **Instruction + Context + Question** pattern:
   ```
   [Role/instruction]

   Context: [Relevant background information]

   Question: [Specific query]
   ```

3. **Output formatting instructions**:
   ```
   Respond in JSON format with keys: recommendation, reasoning, confidence_score
   ```

> [!TIP]
> For StyleCo's customer service, you'll combine techniques: role prompting (fashion expert), few-shot examples (sample Q&A), and structured output (consistent response format).

**Prompting Best Practices:**
- **Be specific**: "Write a professional email" vs "Write a 150-word professional email declining a meeting request, maintaining positive tone"
- **Provide constraints**: Length limits, format requirements, forbidden content
- **Include examples**: Show don't tell - examples are more powerful than descriptions
- **Iterate systematically**: Change one variable at a time to understand what works
- **Test edge cases**: How does it handle ambiguous inputs, unusual requests, or missing information?

#### Recommended Reading

- [Google Gen AI SDK Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/sdks/overview) - Official SDK overview for Python, Go, Node.js, and Java
- [Google Gen AI Python SDK Reference](https://googleapis.github.io/python-genai/) - Detailed Python API reference
- [Google's Prompting Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design) - Official introduction to prompt design
- [Prompt Design Strategies](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies) - Best practices from Google
- [Prompt Engineering Whitepaper (68 pages)](https://www.kaggle.com/whitepaper-prompt-engineering) - Comprehensive deep-dive from Google/Kaggle

### Generation Parameters

Understanding these parameters is essential for controlling model behavior:

| Parameter | Range | Effect |
|-----------|-------|--------|
| **Temperature** | 0.0 - 2.0 | Higher = more creative/random |
| **Top-p** | 0.0 - 1.0 | Nucleus sampling threshold |
| **Top-k** | 1 - 40 | Limits vocabulary per step |
| **Max tokens** | Varies | Output length limit |

> [!NOTE]
> **Rule of thumb**: Use low temperature (0.0-0.3) for factual/deterministic tasks, higher (0.7-1.0) for creative tasks.

### LLM Limitations

Be aware of these inherent limitations - they will inform your design decisions:

| Limitation | Description | Mitigation |
|------------|-------------|------------|
| **Hallucinations** | LLMs can confidently generate false information | RAG, grounding, fact-checking |
| **Knowledge cutoff** | Training data has a date limit | Tool use, real-time data access |
| **No real-time data** | Can't access current information natively | Function calling, MCP servers |
| **Context confusion** | May mix up information in long conversations | Context management, summarization |
| **Prompt injection** | Malicious inputs can manipulate behavior | Input validation, Model Armor |

---

### Project Structure

Navigate to the `cloud_run/genai-api` directory. A basic FastAPI application structure is provided:

```
cloud_run/genai-api/
├── main.py              # FastAPI app entrypoint
├── models/              # Pydantic models for request/response schemas
│   └── __init__.py
├── services/            # Business logic and Gemini API calls
│   └── __init__.py
├── routers/             # Add your endpoints here
│   └── __init__.py
├── pyproject.toml       # Python project configuration
└── Dockerfile           # Container configuration (you should not need to modify)
```

---

## Your Mission

### Hello, Gemini

StyleCo stakeholders aren't convinced about GenAI yet. Your first task is to demonstrate you can successfully connect to the Gemini API.

**Objective**: Create a `/hello_gemini` endpoint that accepts a prompt and returns Gemini's response.

**Requirements**:
- Accept a JSON body with the prompt
- Make a call to Gemini using the [Google Gen AI SDK](https://cloud.google.com/vertex-ai/generative-ai/docs/sdks/overview)
- Return the model's response

**Example request**:
```bash
curl -X POST http://localhost:8080/hello_gemini \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the capital of France?"}'
```

**Example response**:
```json
{
  "response": "The capital of France is Paris."
}
```

---

### StyleCo Customer Service Prompt

Now that you've connected to Gemini, create a dedicated customer service assistant for StyleCo.

**Objective**: Create a `/styleco_assistant` endpoint powered by a carefully crafted system prompt.

**Requirements**:
1. Create/adapt the prompt file `cloud_run/genai-api/instructions/styleco_customer_service.txt` with these characteristics:
   - Professional but friendly tone
   - Knowledgeable about fashion and retail
   - Helpful with common customer queries
   - Admits when it doesn't know something
   - Politely declines requests about competitors

2. Create the endpoint that:
   - Loads the system prompt from the file
   - Accepts user messages
   - Returns the assistant's response

> [!WARNING]
> Never hardcode system prompts in your application code. Externalize them for easier iteration and version control.

---

### Temperature Experiments

To further refine the StyleCo assistant, find the optimal temperature setting for different query types.

**Objective**: Create a `/styleco_assistant_temperature` endpoint that demonstrates temperature effects.

**Requirements**:
- Accept a user message and a `temperatures` parameter (list of floats)
- Return responses for each temperature setting
- Default temperatures: `[0.0, 0.5, 1.0]`

**Example response**:
```json
{
  "prompt": "Suggest a bold outfit for a night out",
  "responses": [
    {"temperature": 0.0, "response": "..."},
    {"temperature": 0.5, "response": "..."},
    {"temperature": 1.0, "response": "..."}
  ]
}
```

---

### Token Analysis Utility

To help StyleCo manage costs and stay within context limits, create a token analysis utility.

**Objective**: Create a utility module `utils/token_analysis.py` with cost estimation capabilities.

**Requirements**:

```python
def analyze_prompt(prompt: str, model_name: str = "gemini-2.0-flash") -> dict:
    """
    Analyze a prompt for token usage and cost.
    
    Returns:
        {
            "token_count": int,
            "estimated_cost_usd": float,
            "context_usage_percent": float,
            "warnings": list[str]
        }
    """
```

**Bonus**: Create a `/token_analysis` endpoint that exposes this functionality via the API.

> [!NOTE]
> Refer to [Vertex AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) for current token costs.

---

### Final Task:

As when it comes to cloud, nothing exists if it is not deployed to the cloud, deploy your FastAPI application to Cloud Run following best practices. See the terraform part in the iac/ folder.
You should see the Cloud Build triggering when pushing to your branch.

---

## Reflection Questions

Before moving to Chapter 2, consider these questions:

1. How would token limits affect a long customer service conversation?
2. What prompting technique would work best for product recommendations?
3. How might hallucinations impact customer trust?
4. What temperature would you use for factual queries vs. creative styling suggestions?

---

## Next Steps

Once you've completed the tasks and documented your observations, you're ready for [Chapter 2: Vertex AI Model Garden](chapter_02.md).

In Chapter 2, you'll explore the different Gemini models available and understand when to use each one for StyleCo's various needs.
