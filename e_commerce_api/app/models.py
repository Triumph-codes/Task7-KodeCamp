from typing import Optional, Dict, Any, List
from sqlmodel import Field, SQLModel, Relationship

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    price: float
    stock: int