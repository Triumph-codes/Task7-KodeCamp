from typing import Optional, Dict, Any, List
from sqlmodel import Field, SQLModel, Relationship

# Existing Models
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = "customer"

    cart: Optional["Cart"] = Relationship(back_populates="user")
    
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    price: float
    stock: int

    cart_items: List["CartItem"] = Relationship(back_populates="product")

class UserCreate(SQLModel):
    username: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str

# New Models for Shopping Cart
class Cart(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    is_active: bool = True

    user: Optional[User] = Relationship(back_populates="cart")
    items: List["CartItem"] = Relationship(back_populates="cart")

class CartItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: int = Field(foreign_key="cart.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(gt=0) # 'gt=0' means the quantity must be greater than zero

    cart: Optional[Cart] = Relationship(back_populates="items")
    product: Optional[Product] = Relationship(back_populates="cart_items")

class CartItemCreate(SQLModel):
    product_id: int
    quantity: int

class CartUpdate(SQLModel):
    items: List[CartItemCreate]