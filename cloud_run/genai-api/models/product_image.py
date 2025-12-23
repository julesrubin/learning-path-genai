import base64
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AspectRatio(str, Enum):
    SQUARE = "1:1"
    LANDSCAPE = "16:9"
    PORTRAIT = "9:16"
    STANDARD = "4:3"
    VERTICAL = "3:4"


class ImageStyle(str, Enum):
    EDITORIAL = "Editorial"
    LIFESTYLE = "Lifestyle"
    PRODUCT_ONLY = "Product-only"
    FLAT_LAY = "Flat-lay"


class ProductImageRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_name: str = Field(..., examples=["Classic Leather Briefcase"])
    setting: str = Field(
        ...,
        examples=["Professional man in modern office with natural lighting"],
    )
    style: ImageStyle = Field(..., examples=["Editorial"])
    aspect_ratio: AspectRatio = Field(default=AspectRatio.SQUARE, examples=["1:1"])
    image_count: int = Field(default=1, ge=1, le=4, examples=[2])
    negative_prompt: Optional[str] = Field(
        default=None,
        examples=["low quality, blurry, distorted"],
    )


class ImageData(BaseModel):
    base64_data: str = Field(..., examples=["/9j/4AAQSkZJRg..."])
    mime_type: str = Field(default="image/png", examples=["image/png"])


class ProductImageResponse(BaseModel):
    images: List[ImageData] = Field(..., examples=[[{"base64_data": "/9j/4AAQSkZJRg...", "mime_type": "image/png"}]])
    prompt_used: str = Field(..., examples=["Editorial fashion photography of Elegance Silk Blouse..."])
    image_count: int = Field(..., examples=[2])
