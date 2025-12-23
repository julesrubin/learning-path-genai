from fastapi import APIRouter

from models.product_description import ProductDescriptionRequest, ProductDescriptionResponse
from services.product_description import ProductDescriptionClient

router = APIRouter()
product_description_client = ProductDescriptionClient()


@router.post("/generate_product_description", response_model=ProductDescriptionResponse)
def generate_product_description(
    product_description_request: ProductDescriptionRequest,
) -> ProductDescriptionResponse:
    """
    Generate a product description based on the provided product information.
    """
    description = product_description_client.generate_product_description(product_description_request)
    return description
