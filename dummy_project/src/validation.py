from typing import Optional
from pydantic import BaseModel

# Pydantic model for the item
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    emi: Optional[float] = None