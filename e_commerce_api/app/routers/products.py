from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session, select

from app.database import get_session
from app.models import Product, User
from app.security import get_current_admin_user

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: Product, 
    session: Session = Depends(get_session),
    admin_user: User = Depends(get_current_admin_user) # Protect this endpoint
):
    """Creates a new product (Admin only)."""
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.get("/", response_model=List[Product])
def get_products(session: Session = Depends(get_session)):
    """Retrieves all products (Public access)."""
    products = session.exec(select(Product)).all()
    return products

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_session)):
    """Retrieves a single product by its ID (Public access)."""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int, 
    product_data: Product, 
    session: Session = Depends(get_session),
    admin_user: User = Depends(get_current_admin_user) # Protect this endpoint
):
    """Updates an existing product (Admin only)."""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.stock = product_data.stock
    
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int, 
    session: Session = Depends(get_session),
    admin_user: User = Depends(get_current_admin_user) # Protect this endpoint
):
    """Deletes a product by its ID (Admin only)."""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    session.delete(product)
    session.commit()
    return None