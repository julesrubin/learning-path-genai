from pydantic import BaseModel, ConfigDict, Field
from enum import Enum
from typing import List

class DescriptionLength(str, Enum):
    SHORT = "Short"
    MEDIUM = "Medium"
    LONG = "Long"

class TargetAudience(str, Enum):
    CHILDREN = "Children"
    TEENS = "Teens"
    ADULTS = "Adults"
    SENIORS = "Seniors"
    PROFESSIONALS = "Professionals"

class ProductDescriptionRequest(BaseModel):
    # Enable V2 specific configurations if needed
    model_config = ConfigDict(from_attributes=True)

    product_name: str = Field(..., examples=["Eco-Friendly Water Bottle"])
    categories: List[str] = Field(..., examples=[["Outdoor", "Fitness", "Sustainability"]])
    materials: List[str] = Field(..., examples=[["Stainless Steel", "Bamboo"]])
    colors: List[str] = Field(..., examples=[["Green", "Blue", "Black"]])
    description_length: DescriptionLength = Field(..., examples=["Medium"])
    target_audience: TargetAudience = Field(..., examples=["Adults"])

class ProductDescriptionResponse(BaseModel):
    description: str = Field(..., examples=["This eco-friendly water bottle is perfect for outdoor enthusiasts..."])
    seo_keywords: List[str] = Field(..., examples=[["eco-friendly", "water bottle", "sustainable"]])
