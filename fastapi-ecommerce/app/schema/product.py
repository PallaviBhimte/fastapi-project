from pydantic import BaseModel, Field
from typing import Annotated
from uuid import UUID

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
            examples = ["734-hjd-378-3d", "asdasd-asd-sad-809"]
        )
    ]
    
    # Product name
    name: str
