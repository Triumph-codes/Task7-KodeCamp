from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models import User, Product, Cart, CartItem, CartItemCreate, CartUpdate, Order, OrderItem
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

@router.post("/checkout", status_code=status.HTTP_201_CREATED)
def checkout(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Processes the checkout for the current user's active cart.
    This creates an order, updates product stock, and clears the cart.
    """
    cart = session.exec(
        select(Cart).where(Cart.user_id == current_user.id, Cart.is_active == True)
    ).first()

    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Your cart is empty.")

    # Validate stock for all items in the cart
    cart_items = session.exec(
        select(CartItem).where(CartItem.cart_id == cart.id)
    ).all()

    total_price = 0
    order_items = []
    
    for item in cart_items:
        product = session.get(Product, item.product_id)
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {product.name}. Available: {product.stock}, Requested: {item.quantity}"
            )
        
        # Calculate price for this item and add to total
        total_price += product.price * item.quantity
        
        # Create a new order item for the final record
        order_item = OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )
        order_items.append(order_item)

    # All checks passed, proceed with the transaction
    try:
        # Create a new order
        order = Order(user_id=current_user.id, total_price=total_price)
        session.add(order)
        session.commit()
        session.refresh(order)

        # Add all order items to the session and link to the new order
        for item in order_items:
            item.order_id = order.id
            session.add(item)
            
        session.commit()
        session.refresh(order)

        # Update product stock and clear the cart
        for item in cart_items:
            product = session.get(Product, item.product_id)
            product.stock -= item.quantity
            session.add(product)
            session.delete(item)
            
        session.delete(cart)
        session.commit()

        return {"message": "Checkout successful!", "order_id": order.id, "total_price": total_price}

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during checkout: {e}"
        )