from fastapi import APIRouter, HTTPException
from google.genai.errors import ClientError

from models.product_image import ProductImageRequest, ProductImageResponse
from services.product_image import ProductImageClient

router = APIRouter()
product_image_client = ProductImageClient()


@router.post("/generate_product_image", response_model=ProductImageResponse)
def generate_product_image(
    request: ProductImageRequest,
) -> ProductImageResponse:
    """
    Generate product images based on the provided product information.

    Args:
        request: ProductImageRequest containing product details and image config.

    Returns:
        ProductImageResponse with generated images and metadata.

    Raises:
        HTTPException: 400 if prompt is blocked by safety filters.
        HTTPException: 500 for other generation errors.
    """
    try:
        return product_image_client.generate_product_image(request)
    except ClientError as e:
        error_message = str(e).lower()
        if "blocked" in error_message or "safety" in error_message:
            raise HTTPException(
                status_code=400,
                detail="Image generation blocked by safety filters. Please modify your prompt to avoid potentially sensitive content.",
            )
        raise HTTPException(
            status_code=500,
            detail=f"Image generation failed: {str(e)}",
        )
    except ValueError as e:
        error_message = str(e).lower()
        # Safety filter errors should return 400, not 500
        if "blocked" in error_message or "safety" in error_message or "filtered" in error_message:
            raise HTTPException(
                status_code=400,
                detail=str(e),
            )
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
