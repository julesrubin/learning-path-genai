from google import genai

from config import settings
from models.product_description import (
    ProductDescriptionRequest,
    ProductDescriptionResponse,
)
from prompts import load_prompt


class ProductDescriptionClient:
    """
    Client for generating product descriptions using Google's Gemini API via Vertex AI.
    """

    def __init__(self):
        """Initialize the Product Description client with Vertex AI configuration."""
        self.client = genai.Client(
            vertexai=True,
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
        )
        self.model_name = settings.gemini_model_name

    def generate_product_description(
        self, product_description_request: ProductDescriptionRequest
    ) -> ProductDescriptionResponse:
        """
        Generate a product description based on the provided product information.

        Args:
            product_description_request (ProductDescriptionRequest): Information about the product.

        Returns:
            ProductDescriptionResponse: Generated product description with SEO keywords.

        Raises:
            ValueError: If the response text is empty or None.
        """
        prompt = load_prompt(
            "product_description",
            product_name=product_description_request.product_name,
            categories=", ".join(product_description_request.categories),
            materials=", ".join(product_description_request.materials),
            colors=", ".join(product_description_request.colors),
            description_length=product_description_request.description_length.value,
            target_audience=product_description_request.target_audience.value,
        )

        config = genai.types.GenerateContentConfig(
            response_mime_type="application/json",
            response_json_schema=ProductDescriptionResponse.model_json_schema(),
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config,
        )

        if not response.text:
            raise ValueError("Empty response from Gemini API")

        return ProductDescriptionResponse.model_validate_json(response.text)
