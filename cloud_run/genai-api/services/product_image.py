import base64
import os
from typing import List

from google import genai
from google.genai.types import GenerateImagesConfig

from models.product_image import (
    ImageData,
    ProductImageRequest,
    ProductImageResponse,
)


class ProductImageClient:
    """
    Client for generating product images using Google's Imagen API via Vertex AI.
    Handles initialization and image generation with configurable parameters.
    """

    def __init__(self):
        """Initialize the Product Image client with Vertex AI configuration."""
        self.client = self._initialize_client()
        self.model_name = "imagen-4.0-generate-001"

    def _initialize_client(self) -> genai.Client:
        """
        Initialize and return a Gemini client configured for Vertex AI.

        Returns:
            Configured genai.Client instance
        """
        return genai.Client(
            vertexai=True,
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "europe-west1"),
        )

    def _build_prompt(self, request: ProductImageRequest) -> str:
        """
        Build a coherent image generation prompt from request parameters.

        Args:
            request: The product image request containing product details.

        Returns:
            A formatted prompt string for image generation.
        """
        prompt_parts = [
            f"{request.style.value} fashion photography of {request.product_name}.",
            f"Setting: {request.setting}.",
            "High quality, detailed, professional lighting.",
        ]
        return " ".join(prompt_parts)

    def generate_product_image(
        self, request: ProductImageRequest
    ) -> ProductImageResponse:
        """
        Generate product images based on the provided request parameters.

        Args:
            request: ProductImageRequest containing product details and image config.

        Returns:
            ProductImageResponse with base64-encoded images and metadata.

        Raises:
            ValueError: If the response contains no images.
            ClientError: If the prompt is blocked by safety filters.
        """
        prompt = self._build_prompt(request)

        config = GenerateImagesConfig(
            number_of_images=request.image_count,
            aspect_ratio=request.aspect_ratio.value,
            negative_prompt=request.negative_prompt,
        )

        response = self.client.models.generate_images(
            model=self.model_name,
            prompt=prompt,
            config=config,
        )

        if not response.generated_images:
            raise ValueError("No images generated from Imagen API")

        images: List[ImageData] = []
        for i, generated_image in enumerate(response.generated_images):
            image_bytes = generated_image.image.image_bytes
            base64_data = base64.b64encode(image_bytes).decode("utf-8")
            images.append(
                ImageData(
                    base64_data=base64_data,
                    mime_type="image/png",
                )
            )
            # save the image locally for debugging purposes
            with open(f"debug_image_{i}.png", "wb") as img_file:
                img_file.write(image_bytes)

        return ProductImageResponse(
            images=images,
            prompt_used=prompt,
            image_count=len(images),
        )
