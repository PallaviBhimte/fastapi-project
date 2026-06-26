from pydantic import (
    BaseModel, 
    Field, 
    AnyUrl, 
    field_validator, 
    model_validator, 
    computed_field
)
from typing import Annotated, Literal, Optional, List
from uuid import UUID
from datetime import datetime

# Product data model with validation rules
class Product(BaseModel):
    
    # Unique product identifier (UUID format)
    id: UUID
    
    # Stock Keeing Unit with validation
    sku: Annotated[
        str,
        Field(
            min_length = 6, 
            max_length=30, 
            title= "SKU", 
            description = "Stock Keeping Unit", 
            examples = ["XIAO-359GB-001", "APPL-212GB-049"]
        )
    ]
    
    # Product name
    name: Annotated[
        str,
        Field(
            min_length = 3,
            max_length = 80,
            title = "Product Name",
            description = "Readable product name (3-80 chars).",
            examples = ["Xiaomi Model Pro", "Apple Model X"]
        )
    ]
    
    # Short product description
    description: Annotated[
        str,
        Field(
            max_length = 200,
            description = "Short product description"
        )
    ]
    
    # Product category
    category: Annotated[
        str,
        Field(
           min_length = 3,
           max_length = 30,
           description = "Category like mobiles/laptops/electronics/accessories",
           examples = ["mobiles", "laptops"]
        )
    ]
    
    # Product brand
    brand: Annotated[
        str,
        Field(
            min_length = 2,
            max_length = 40,
            examples = ["Xiaomi", "Apple"]  
        )
    ]
    
    # Product price
    price: Annotated[
        float,
        Field(
            gt = 0,
            strict = True,
            description = "Base price"
        )
    ]
    
    # Supported currency
    currency: Literal["INR"] = "INR"
    
    # Discount percentage (0-90%)
    discount_percent: Annotated[
        int,
        Field(
            ge = 0,
            le = 90,
            description = "Discount in percent (0-90)"
        )
    ] = 0

    # Available stocky quantity
    stock: Annotated[
        int,
        Field(
            ge = 0,
            description = "Available stock (>=0)"
        )
    ]
    
    # Product availability status
    is_active: Annotated[
        bool,
        Field(
            description = "Is product active?"
        )
    ]
    
    # Product rating out of 5
    rating: Annotated[
        float,
        Field(
            ge = 0,
            le = 5,
            strict = True,
            description = "Rating out of 5"
        )
    ]
    
    # Optional product tags
    tags: Annotated[
        Optional[List[str]],
        Field(
            default = None,
            max_length = 10,
            description = "Upto 10 tags"
        )
    ]
    
    # Product image URLs
    image_urls: Annotated[
        List[AnyUrl],
        Field(
            max_length = 1,
            description = "Atleast 1 image URL"
        )
    ]
    
    # Product creation timestamp
    created_at: datetime
    
    # Validate SKU format
    @field_validator("sku", mode = "after")
    @classmethod
    def validate_sku_format(cls, value:str):
        if "-" not in value:
            raise ValueError("SKU must have '-'")
        last = value.split("-")[-1]
        if not (len(last) == 3 and last.isdigit()):
            raise ValueError("SKU must end with a 3-digit sequence like '-234'")
        return value
    
    # Validate cross-field business rules
    @model_validator(mode="after")
    @classmethod
    def validate_business_rules(cls, model:"Product"):
        if model.stock == 0 and model.is_active is True:
            raise ValueError("If stock is 0, is_active must be False")
        
        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError("Discounted product must have the a rating (rating != 0)")
        return model
    
    # Calculate discounted price
    @computed_field
    @property
    def final_price(self) -> float:
        return round(self.price * (1 - self.discount_percent / 100), 2)