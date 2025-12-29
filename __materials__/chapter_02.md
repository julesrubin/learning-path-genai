# Chapter 2: Vertex AI Model Garden

## Context: Expanding StyleCo's AI Capabilities

StyleCo's initial customer service AI Assistant has impressed stakeholders. Now, the marketing team wants in on the action.

### The Business Challenge

**Product Description Generation**: StyleCo's catalog has 50,000+ products. Writing compelling, SEO-friendly descriptions for each takes significant copywriter time. They want to automate this process while maintaining brand voice.

### Your Role

In this chapter, you'll:

1. **Explore Google's Model Garden** to understand available models and their capabilities
2. **Implement a product description generator** using Gemini's text generation with structured output
3. **Implement a product image generator** using Imagen for marketing visuals
4. **Learn key techniques**: Jinja2 templates, Pydantic enums, JSON schema enforcement, and image generation

---

## Learning Resources

### Vertex AI Model Garden Overview

The [Vertex AI Model Garden](https://cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models) is Google Cloud's central hub for discovering and deploying AI models. It provides access to:

- **Google's foundation models**: Gemini, Imagen, Chirp (speech), etc.
- **Google's partners proprietary models**: Anthropic Claude, Cohere, etc.
- **Open-source models**: Llama, Mistral, Deepseek, etc.
- **Fine-tuned variants**: Specialized versions for specific tasks

> [!TIP]
> Explore the [Model Garden in the Google Cloud Console](https://console.cloud.google.com/vertex-ai/model-garden) to see all available models and their capabilities.

### Gemini Model Family

The Gemini family offers models optimized for different use cases:

| Model                     | Best For                                             | Context Window | Key Strengths                     |
| ------------------------- | ---------------------------------------------------- | -------------- | --------------------------------- |
| **Gemini 2.5 Pro**        | Complex reasoning, coding, analysis                  | 1M tokens      | Highest capability, deep thinking |
| **Gemini 2.5 Flash**      | Best for balancing reasoning and speed               | 1M tokens      | Cost-effective, fast              |
| **Gemini 2.5 Flash-Lite** | Most balanced Gemini model for low latency use cases | 1M tokens      | Fastest, lowest cost              |

**Choosing the Right Model:**

- **Flash models**: Use for high-volume, cost-sensitive applications (like StyleCo's customer service)
- **Pro models**: Use for complex tasks requiring deeper reasoning (like detailed product analysis)

> [!NOTE]
> Model availability and capabilities evolve rapidly. Always check the [latest documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/migrate) for current specifications.

### Imagen: Image Generation

[Imagen](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview) is Google's text-to-image model for generating high-quality images:

**Capabilities:**

- **Text-to-image**: Generate images from text descriptions
- **Image editing**: Modify existing images based on prompts
- **Inpainting/Outpainting**: Fill in or extend images
- **Upscaling**: Enhance image resolution

**Key Parameters:**
| Parameter | Description |
|-----------|-------------|
| `prompt` | Text description of the desired image |
| `sampleCount` | How many variations to generate (1-4) |
| `aspectRatio` | Image dimensions (1:1, 16:9, 9:16, 4:3, 3:4) |
| `negativePrompt` | What to avoid in the generated image |
| `sampleImageSize` | Output resolution: `"1K"` (default) or `"2K"` |
| `seed` | For reproducible generations (requires `addWatermark: false`) |

> [!IMPORTANT]
> Imagen has safety filters that may block certain prompts. Always handle potential content policy exceptions in your code.

### Multimodal Capabilities

Gemini models are natively multimodal, meaning they can process and understand multiple types of input:

**Input Types:**

- Text
- Images (JPEG, PNG, GIF, WebP)
- Audio (MP3, WAV, FLAC)
- Video (MP4, MOV)
- Documents (PDF)

---

## Your Mission

### Product Description Generator

StyleCo needs to generate compelling product descriptions at scale. Create an endpoint that takes basic product information and generates marketing-ready descriptions.

**Objective**: Create a `/generate_product_description` endpoint that generates rich product descriptions.

**Requirements**:

- Accept product details (name, categories, materials, colors, target audience)
- Generate SEO-friendly descriptions in the StyleCo brand voice
- Support multiple description lengths (Short, Medium, Long)
- Return structured JSON with description and SEO keywords

**Example request**:

```bash
curl -X POST http://localhost:8080/generate_product_description \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Elegance Silk Blouse",
    "categories": ["Tops", "Workwear", "Evening"],
    "materials": ["100% Mulberry Silk"],
    "colors": ["Ivory", "Navy", "Blush Pink"],
    "description_length": "Short",
    "target_audience": "Professionals"
  }'
```

**Example response**:

```json
{
  "description": "Experience unparalleled comfort and sophisticated grace with the Elegance Silk Blouse. Crafted from 100% pure Mulberry Silk, its buttery soft texture and luminous drape effortlessly elevate any ensemble. This versatile piece transitions flawlessly from critical boardroom presentations to elegant evening soirees, pairing exquisitely with tailored trousers or a sleek skirt. A timeless essential for the modern professional.",
  "seo_keywords": [
    "mulberry silk blouse",
    "luxury workwear top",
    "women's silk shirt",
    "elegant evening blouse",
    "professional apparel"
  ]
}
```

> [!TIP]
> Create a dedicated Jinja2 template at `cloud_run/genai-api/instructions/product_description.j2` for the product description generator. This separates prompt engineering from code and makes iteration easy.

#### Implementation Details

**1. Pydantic Models** (`models/product_description.py`):

- Use `Enum` classes for `DescriptionLength` (Short/Medium/Long) and `TargetAudience` (Children/Teens/Adults/Seniors/Professionals)
- Include `Field(..., examples=[...])` for auto-generated OpenAPI documentation

**2. Jinja2 Prompt Template** (`instructions/product_description.j2`):

Read [this article](https://medium.com/@alecgg27895/jinja2-prompting-a-guide-on-using-jinja2-templates-for-prompt-management-in-genai-applications-e36e5c1243cf) for best practices on using Jinja2 with GenAI.

**3. Structured Input/Output**:

- Use `ProductDescriptionRequest` for input validation and then populate the Jinja2 template with the request data
- Use `genai.types.GenerateContentConfig` with `response_json_schema` for structured output
- Validate response with `ProductDescriptionResponse.model_validate_json()`. This guarantees valid JSON output matching your Pydantic model.

---

### Product Image Generator

StyleCo's marketing team wants to generate product lifestyle images for social media and catalog previews. Create an endpoint that generates images based on product descriptions.

**Objective**: Create a `/generate_product_image` endpoint that generates marketing-ready product images using Imagen.

**Requirements**:

- Accept product details (name, setting, style) and image parameters (aspect ratio, count)
- Generate high-quality lifestyle images suitable for marketing
- Support multiple aspect ratios for different platforms (Instagram, website banner, etc.)
- Return base64-encoded images with metadata
- Handle Imagen's safety filters gracefully

**Example request**:

```bash
curl -X POST http://localhost:8080/generate_product_image \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Classic Leather Briefcase",
    "setting": "Professional man in modern office with natural lighting",
    "style": "Editorial",
    "aspect_ratio": "1:1",
    "image_count": 2,
    "negative_prompt": "low quality, blurry, distorted"
  }'
```

**Example response**:

```json
{
  "images": [
    {
      "base64_data": "/9j/4AAQSkZJRg...",
      "mime_type": "image/png"
    },
    {
      "base64_data": "/9j/4AAQSkZJRg...",
      "mime_type": "image/png"
    }
  ],
  "prompt_used": "Editorial fashion photography of Classic Leather Briefcase. Setting: Professional man in modern office with natural lighting. High quality, detailed, professional lighting.",
  "image_count": 2
}
```

> [!WARNING]
> Imagen has strict content safety filters. Some prompts may be blocked. You **must** implement proper error handling for RAI (Responsible AI) filtering to provide meaningful feedback to users.

#### Implementation Details

**1. Pydantic Models** (`models/product_image.py`):

- Use `Enum` for `AspectRatio` (1:1, 16:9, 9:16, 4:3, 3:4) and `ImageStyle` (Editorial, Lifestyle, Product-only, Flat-lay)
- Include `Field(..., ge=1, le=4)` for `image_count` to enforce Imagen's limits
- Create `ImageData` model for individual image responses with `base64_data` and `mime_type`

**2. Imagen Client** (`services/product_image.py`):

Using the Pydantic Settings pattern from Chapter 1, add Imagen-specific configuration:

**First, update `config/settings.py`**:
```python
class Settings(BaseSettings):
    # ... existing Google Cloud and Gemini settings ...
    
    # Imagen Configuration
    imagen_model_name: str = "imagen-4.0-generate-001"
    save_debug_images: bool = False  # Enable for local development
```

**Then, use it in your service**:
```python
from google import genai
from google.genai.types import GenerateImagesConfig
from config import settings

class ProductImageClient:
    def __init__(self):
        self.client = self._initialize_client()
        self.model_name = settings.imagen_model_name

    def _initialize_client(self) -> genai.Client:
        return genai.Client(
            vertexai=True,
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
        )
```

**Conditional Debug Image Saving**:
```python
# In your image generation loop
if settings.save_debug_images:
    with open(f"debug_image_{i}.png", "wb") as img_file:
        img_file.write(image_bytes)
```

> [!TIP]
> The `save_debug_images` flag is useful during development but should be `False` in production to avoid filling up disk space. Control it via environment variable: `SAVE_DEBUG_IMAGES=true`

> [!NOTE]
> Multiple Imagen 4 models are available: `imagen-4.0-generate-001` (standard), `imagen-4.0-ultra-generate-001` (highest quality), and `imagen-4.0-fast-generate-001` (lowest latency). Choose based on your quality/speed requirements.

**3. Image Generation**:

- Use `client.models.generate_images()` for image generation
- Build prompts by combining product name, setting, and style
- Apply `negative_prompt` to filter unwanted image characteristics
- Convert generated images to base64 for API response

```python
response = self.client.models.generate_images(
    model=self.model_name,
    prompt=prompt,
    config=GenerateImagesConfig(
        number_of_images=image_count,  # 1-4
        aspect_ratio=aspect_ratio,      # "1:1", "16:9", etc.
        negative_prompt=negative_prompt,
        image_size="2K",                # "1K" or "2K"
    ),
)

# Access generated images
for generated_image in response.generated_images:
    image_bytes = generated_image.image.image_bytes
    # Convert to base64 for API response
```

**4. Error Handling - Imagen RAI Filtering**:

Understanding how Imagen's RAI (Responsible AI) filters work is crucial for building robust applications.

**The Challenge**:

Unlike typical API errors that raise exceptions, Imagen's safety filters return a **successful 200 response** with blocked content. This can cause your code to crash unexpectedly if you don't handle it properly.

**What Happens When Content is Blocked**:

```python
# Response structure when RAI filters block content:
response.generated_images = [
    GeneratedImage(
        image=Image(),  # Empty Image object!
        rai_filtered_reason="Unable to show generated images. All images were filtered out because they violated Google's Responsible AI practices. Try rephrasing the prompt. If you think this was an error, send feedback. Support codes: 63429089, 64151117",
        safety_attributes=SafetyAttributes()
    )
]

# Key observations:
# - generated_images list is NOT empty ✓
# - But image.image_bytes is None ✗
# - rai_filtered_reason contains the error message ✓
```

**Without proper handling, you'll get**:
```python
image_bytes = generated_image.image.image_bytes  # None
base64.b64encode(image_bytes)  # TypeError: a bytes-like object is required, not 'NoneType'
```

**Proper Implementation** (in `services/product_image.py`):

```python
def generate_product_image(self, request: ProductImageRequest) -> ProductImageResponse:
    """Generate product images with proper RAI error handling."""
    
    response = self.client.models.generate_images(
        model=self.model_name,
        prompt=prompt,
        config=config,
    )

    # CHECK 1: Response has images array
    if not response.generated_images:
        raise ValueError("No images generated from Imagen API")

    images = []
    for i, generated_image in enumerate(response.generated_images):
        # CHECK 2: RAI filtering - check this FIRST
        if generated_image.rai_filtered_reason:
            raise ValueError(
                f"Content blocked by safety filters: {generated_image.rai_filtered_reason}"
            )
        
        # CHECK 3: Image data exists (double safety check)
        if not generated_image.image or not generated_image.image.image_bytes:
            raise ValueError(
                "No image data returned. This may be due to content safety filters."
            )
        
        # Now it's safe to process the image
        image_bytes = generated_image.image.image_bytes
        base64_data = base64.b64encode(image_bytes).decode("utf-8")
        images.append(ImageData(base64_data=base64_data, mime_type="image/png"))
        
        # Conditional debug saving
        if settings.save_debug_images:
            with open(f"debug_image_{i}.png", "wb") as img_file:
                img_file.write(image_bytes)

    return ProductImageResponse(
        images=images,
        prompt_used=prompt,
        image_count=len(images),
    )
```

**Router Layer** (in `routers/product_image.py`):

The router should handle the ValueError from the service and convert it to an appropriate HTTP response:

```python
from fastapi import APIRouter, HTTPException

@router.post("/generate_product_image", response_model=ProductImageResponse)
def generate_product_image(request: ProductImageRequest) -> ProductImageResponse:
    try:
        return product_image_client.generate_product_image(request)
    except ValueError as e:
        # Safety filter errors and validation errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
```

> [!IMPORTANT]
> **Why this architecture matters**:
> - **Service layer** contains business logic and error detection
> - **Router layer** handles HTTP concerns (status codes, responses)
> - **ValueError** signals user-correctable errors (400 Bad Request)
> - **Exception** catches unexpected errors (500 Internal Server Error)

**Testing Your Error Handling**:

To verify your implementation works correctly, test with prompts that trigger safety filters:

```python
# Test cases that should return 400 with clear error messages:
test_prompts = [
    "political figure in controversial context",
    "violent or weapon-related imagery",
    "explicit or adult content",
    "copyrighted characters or brands"
]
```

Expected behavior:
- ✅ Returns HTTP 400 (Bad Request)
- ✅ Clear error message with RAI filter reason
- ✅ No TypeErrors or crashes
- ✅ Logs contain useful debugging information

> [!TIP]
> Create a simple test notebook (like the `test.ipynb` example in your repo) to quickly test various prompts and see RAI filter responses without going through the full API.

> [!TIP]
> Test your image generation endpoint with various prompts to understand Imagen's capabilities and limitations. Start with simple, descriptive prompts and gradually add complexity.

---

## Bonus Challenges

### Challenge 1: Multimodal Product Analysis

Combine Gemini's multimodal capabilities with your existing endpoints. Create an endpoint that accepts a product image and generates a description based on visual analysis.

**Objective**: Create a `/analyze_product_image` endpoint that uses Gemini's vision capabilities.

**Hints**:
- Accept image as base64 or URL
- Use `genai.types.Part.from_image()` to include images in prompts
- Combine visual analysis with your existing description generation template

### Challenge 2: Prompt Enhancement Pipeline

Create a pipeline that improves user prompts before sending them to Imagen.

**Objective**: Use Gemini to enhance simple prompts into detailed, photography-focused descriptions.

**Example flow**:
1. User provides: "silk blouse on model"
2. Gemini enhances to: "Editorial fashion photography of an elegant silk blouse worn by a professional model. Soft natural lighting from a large window, neutral background, shallow depth of field. High-end fashion magazine aesthetic."
3. Enhanced prompt sent to Imagen

---

## Deploy to Cloud Run

As you correctly deployed to Cloud Run in Chapter 1, you should just need to commit your changes and push to trigger the deployment.

---

## Reflection Questions

Before moving to Chapter 3, consider these questions:

1. How did using Jinja2 templates improve your prompt engineering process?
2. What challenges did you face when implementing structured output with JSON schemas?
3. **How does Pydantic Settings improve code maintainability compared to direct `os.getenv()` calls?**
4. **Why is it important to check `rai_filtered_reason` before accessing `image_bytes` in Imagen responses?**
5. What potential use cases can you envision for multimodal models in your applications?
6. How would you optimize costs when using high-volume models like Gemini and Imagen in production?
7. What strategies would you use to handle content safety filters effectively in a user-facing application?

---

## Next Steps

Once you've completed the tasks and documented your observations, you're ready for [Chapter 3: RAG with Vertex AI Search](chapter_03.md).

In Chapter 3, you'll explore how to build Retrieval-Augmented Generation (RAG) applications using Vertex AI Search, enabling your applications to provide accurate and contextually relevant responses by leveraging external knowledge bases.
