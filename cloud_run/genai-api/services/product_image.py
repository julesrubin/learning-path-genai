import base64

from google import genai
from google.genai.types import GenerateImagesConfig

from config import settings
from models.product_image import (
    ImageData,
    ProductImageRequest,
    ProductImageResponse,
)
from prompts import load_prompt


class ProductImageClient:
    """
    Client for generating product images using Google's Imagen API via Vertex AI.
    """

    def __init__(self):
        """Initialize the Product Image client with Vertex AI configuration."""
        self.client = genai.Client(
            vertexai=True,
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
        )
        self.model_name = settings.imagen_model_name

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
            ValueError: If the response contains no images or content is blocked by safety filters.
        """
        prompt = load_prompt(
            "product_image",
            style=request.style.value,
            product_name=request.product_name,
            setting=request.setting,
        )

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

        images: list[ImageData] = []
        for i, generated_image in enumerate(response.generated_images):
            if generated_image.rai_filtered_reason:
                raise ValueError(
                    f"Content blocked by safety filters: {generated_image.rai_filtered_reason}"
                )

            if not generated_image.image or not generated_image.image.image_bytes:
                raise ValueError(
                    "No image data returned. This may be due to content safety filters."
                )

            image_bytes = generated_image.image.image_bytes
            base64_data = base64.b64encode(image_bytes).decode("utf-8")
            images.append(
                ImageData(
                    base64_data=base64_data,
                    mime_type="image/png",
                )
            )
            if settings.save_debug_images:
                with open(f"debug_image_{i}.png", "wb") as img_file:
                    img_file.write(image_bytes)

        return ProductImageResponse(
            images=images,
            prompt_used=prompt,
            image_count=len(images),
        )
