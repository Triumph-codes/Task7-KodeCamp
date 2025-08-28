from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models import User, Product, Cart, CartItem, CartItemCreate, CartUpdate
from app.security import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

def get_or_create_cart(user_id: int, session: Session) -> Cart:
    """Helper function to get or create an active cart for a user."""
    cart = session.exec(
        select(Cart).where(Cart.user_id == user_id, Cart.is_active == True)
    ).first()
    if not cart:
        cart = Cart(user_id=user_id)
        session.add(cart)
        session.commit()
        session.refresh(cart)
    return cart

@router.post("/add-item", status_code=status.HTTP_201_CREATED)
def add_item_to_cart(
    item_in: CartItemCreate, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Adds a product to the user's shopping cart."""
    product = session.get(Product, item_in.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < item_in.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available.")

    cart = get_or_create_cart(current_user.id, session)

    # Check if item is already in cart
    existing_item = session.exec(
        select(CartItem).where(
            CartItem.cart_id == cart.id, CartItem.product_id == item_in.product_id
        )
    ).first()

    if existing_item:
        existing_item.quantity += item_in.quantity
        session.add(existing_item)
    else:
        new_item = CartItem(
            cart_id=cart.id, product_id=item_in.product_id, quantity=item_in.quantity
        )
        session.add(new_item)

    session.commit()
    session.refresh(cart)
    return {"message": "Item added to cart successfully."}

@router.get("/", response_model=List[CartItem])
def get_cart_items(
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    """Retrieves the current user's active shopping cart items."""
    cart = session.exec(
        select(Cart).where(Cart.user_id == current_user.id, Cart.is_active == True)
    ).first()
    if not cart:
        return []

    return cart.items

@router.delete("/remove-item/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item_from_cart(
    item_id: int, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Removes a specific item from the user's shopping cart."""
    cart = get_or_create_cart(current_user.id, session)
    cart_item = session.exec(
        select(CartItem).where(CartItem.id == item_id, CartItem.cart_id == cart.id)
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart.")

    session.delete(cart_item)
    session.commit()
    return None

@router.put("/update-item/{item_id}")
def update_item_in_cart(
    item_id: int,
    quantity: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Updates the quantity of an item in the user's cart."""
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero.")
    
    cart = get_or_create_cart(current_user.id, session)
    cart_item = session.exec(
        select(CartItem).where(CartItem.id == item_id, CartItem.cart_id == cart.id)
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart.")

    product = session.get(Product, cart_item.product_id)
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available for this quantity.")
        
    cart_item.quantity = quantity
    session.add(cart_item)
    session.commit()
    session.refresh(cart_item)
    return cart_item