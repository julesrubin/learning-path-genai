from pathlib import Path

from google import genai
from jinja2 import Environment, FileSystemLoader

from config import settings
from models.product_description import (
    ProductDescriptionRequest,
    ProductDescriptionResponse,
)


class ProductDescriptionClient:
    """
    Client for generating product descriptions using Google's Gemini API via Vertex AI.
    Handles initialization and prompt generation with Jinja2 templates.
    """

    def __init__(self):
        """Initialize the Product Description client with Vertex AI configuration."""
        self.client = self._initialize_client()
        self.prompts_dir = Path(__file__).parent.parent / "instructions"
        self.model_name = settings.gemini_model_name

        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.prompts_dir),
            autoescape=False,  # No HTML escaping needed for prompts
        )

    def _initialize_client(self) -> genai.Client:
        """
        Initialize and return a Gemini client configured for Vertex AI.

        Returns:
            Configured genai.Client instance
        """
        return genai.Client(
            vertexai=True,
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
        )

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
        # Load and render the Jinja2 template
        template = self.jinja_env.get_template("product_description.j2")
        prompt = template.render(
            product_name=product_description_request.product_name,
            categories=", ".join(product_description_request.categories),
            materials=", ".join(product_description_request.materials),
            colors=", ".join(product_description_request.colors),
            description_length=product_description_request.description_length,
            target_audience=product_description_request.target_audience,
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
