from pydantic import (
    BaseModel, 
    Field, 
    AnyUrl, 
    field_validator, 
    model_validator, 
    computed_field,
    EmailStr
)
from typing import Annotated, Literal, Optional, List
from uuid import UUID
from datetime import datetime

# Seller data model 
class Seller(BaseModel):
    
    # Unique seller identifier (UUID format)
    id: UUID
    
    # Seller name
    name: Annotated[
        str,
        Field(
            min_length = 2,
            max_length = 60,
            title = "Seller Name",
            description = "Name of the Seller (2-60 chars).",
            examples = ["Mi Store", "Apple Store Australia"]
        )
    ]
    
    # Seller Email
    email: EmailStr
    
    # Seller website URL
    website: AnyUrl
    
    # Allow only approved seller email domains
    @field_validator("email", mode = "after")
    @classmethod
    def validate_seller_email_format(cls, value:EmailStr):
        allowed_domains = {
            "mistore.in",
            "realmeofficial.in",
            "samsungindia.in",
            "lenovostore.in",
            "hpworld.in",
            "applestoreindia.in",
            "dellexclusive.in",
            "sonycenter.in",
            "oneplusstore.in",
            "asusexclusive.in"   
        }
        
        # Extract email domain
        domain = str(value).split("@")[-1].lower()
        
        # Validate domain against allowlist
        if domain not in allowed_domains:
            raise ValueError(f"Seller email domain '{domain}' is not allowed. Allowed domains: {allowed_domains}")
        return value

# Product dimensions in centimeters
class DimensionCM(BaseModel):
    
    # Product length
    length: Annotated[
        float,
        Field(
            gt = 0,
            strict = True,
            description = "Length in cm"
        )
    ]
    
    # Product width
    width: Annotated[
        float,
        Field(
            gt = 0,
            strict = True,
            description = "Width in cm"
        )
    ]
    
    # Product height
    height: Annotated[
        float,
        Field(
            gt = 0,
            strict = True,
            description = "Height in cm"
        )
    ]
    
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
    
    # Dimension
    dimensions_cm: DimensionCM
    
    # Seller
    seller: Seller
    
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
    
    # Calculate product volume in cubic centimeters (L × W × H)
    @computed_field
    @property
    def volume_cm3(self) -> float:
        d = self.dimensions_cm
        return round(d.length * d.width * d.height, 2)