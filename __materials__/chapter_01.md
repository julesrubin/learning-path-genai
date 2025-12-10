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

Before writing any code, invest time understanding the fundamentals.

#### Tokens and Tokenization

LLMs don't see text the way humans do - they process **tokens** (subword units):
- The word "tokenization" might become `["token", "ization"]`
- Different models use different tokenizers
- Token count directly affects cost and context limits

> [!TIP]
> Use the [Gemini tokenizer playground](https://ai.google.dev/gemini-api/docs/tokens) to see how your text gets tokenized.

#### Embeddings and Vector Space

Text is converted to high-dimensional vectors called **embeddings**:
- Semantically similar text has similar vectors
- This mathematical representation enables similarity search
- Embeddings are the foundation of RAG (Chapters 4-5)

#### Context Windows

The context window is the "memory" of a conversation:
- **Gemini 2.0 Flash**: up to 1M tokens
- **Gemini 2.5 Pro**: up to 1M tokens
- Larger context = higher cost and potentially slower responses

> [!IMPORTANT]
> Strategic context management is crucial for production applications. You'll learn techniques for this throughout the learning path.

### Prompting Techniques

| Technique | Description | When to Use |
|-----------|-------------|-------------|
| **Zero-shot** | No examples, just instructions | Simple, well-defined tasks |
| **Few-shot** | Include examples in prompt | When format/style matters |
| **Chain-of-thought** | Ask model to reason step-by-step | Complex reasoning tasks |
| **Role prompting** | Assign a persona | Consistent tone/expertise |

#### Recommended Reading

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

Navigate to the `cloud_run/styleco_api` directory. A basic FastAPI application structure is provided:

```
cloud_run/genai-api/
├── main.py              # FastAPI app entrypoint
├── routers/             # Add your endpoints here
│   └── __init__.py
├── pyproject.toml       # Python project configuration
└── Dockerfile           # Container configuration
```

---

## Your Mission

### Hello, Gemini

StyleCo stakeholders aren't convinced about GenAI yet. Your first task is to demonstrate you can successfully connect to the Gemini API.

**Objective**: Create a `/hello_gemini` endpoint that accepts a prompt and returns Gemini's response.

**Requirements**:
- Accept a JSON body with the prompt and optional generation parameters
- Make a call to Gemini using the Vertex AI SDK
- Return the model's response

**Example request**:
```bash
curl -X POST http://localhost:8080/hello_gemini \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the capital of France?"}'
```

---

### StyleCo Customer Service Prompt

Now that you've connected to Gemini, create a dedicated customer service assistant for StyleCo.

**Objective**: Create a `/styleco_assistant` endpoint powered by a carefully crafted system prompt.

**Requirements**:
1. Create/adapt the prompt file `prompts/styleco_customer_service.txt` with these characteristics:
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

### Prompting Technique Experiments

StyleCo's team has complex questions that the basic assistant struggles with. They want you to experiment with advanced prompting techniques.

**Objective**: Create a `/styleco_assistant_advanced` endpoint that handles complex, multi-faceted queries.

**Test query**: 
> "I'm going to a summer wedding in Italy. I'm a size M and prefer sustainable fashion. What should I wear?"

**Requirements**:
Implement at least two prompting techniques and compare results:

1. **Few-shot prompting**: Include 2-3 example Q&A pairs in your prompt
2. **Chain-of-thought**: Instruct the model to reason step-by-step before answering

**Deliverable**: Document your observations in a `notes/chapter_01_experiments.md` file:
- Which technique produced better recommendations?
- How did response length and quality differ?
- What trade-offs did you observe?

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
See the Cloud Build triggering when pushing to your branch.

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
