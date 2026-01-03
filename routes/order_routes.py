"""
Order management routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from models import Order, OrderItem, Product, User, OrderStatus, UserRole
from auth import get_current_user, require_buyer, require_seller

router = APIRouter(prefix="/api/orders", tags=["Orders"])

# Pydantic models
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    buyer_id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() + 'Z' if v else None
        }

class SellerOrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    price: float
    order_id: int
    buyer_email: str
    order_status: OrderStatus
    
    class Config:
        from_attributes = True

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(require_buyer),
    db: Session = Depends(get_db)
):
    """
    Create a new order (buyer only).
    
    Args:
        order_data: Order creation data with items
        current_user: Current authenticated buyer
        db: Database session
        
    Returns:
        Created order object
        
    Raises:
        HTTPException: If product not found or insufficient stock
    """
    if not order_data.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must contain at least one item"
        )
    
    total_amount = 0
    order_items = []
    
    # Validate products and calculate total
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.product_id} not found"
            )
        
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.name}"
            )
        
        item_total = product.price * item.quantity
        total_amount += item_total
        
        order_items.append({
            "product_id": product.id,
            "quantity": item.quantity,
            "price": product.price
        })
        
        # Update product stock
        product.stock -= item.quantity
    
    # Create order
    new_order = Order(
        buyer_id=current_user.id,
        total_amount=total_amount,
        status=OrderStatus.PENDING
    )
    
    db.add(new_order)
    db.flush()  # Get order ID before adding items
    
    # Create order items
    for item_data in order_items:
        order_item = OrderItem(
            order_id=new_order.id,
            **item_data
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(new_order)
    
    return new_order

@router.get("", response_model=List[OrderResponse])
def get_user_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all orders for the current user.
    Only buyers can see their own orders.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of user's orders
    """
    if current_user.role != UserRole.BUYER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only buyers can view their orders"
        )
    
    orders = db.query(Order).filter(Order.buyer_id == current_user.id).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific order by ID.
    
    Args:
        order_id: Order ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Order object
        
    Raises:
        HTTPException: If order not found or not owned by user
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if current_user.role == UserRole.BUYER and order.buyer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own orders"
        )
    
    return order

@router.get("/seller/orders", response_model=List[SellerOrderItemResponse])
def get_seller_orders(
    current_user: User = Depends(require_seller),
    db: Session = Depends(get_db)
):
    """
    Get all order items for products sold by the current seller.
    
    Args:
        current_user: Current authenticated seller
        db: Database session
        
    Returns:
        List of order items for seller's products
    """
    # Get all order items for seller's products
    order_items = db.query(OrderItem).join(Product).join(Order).join(User).filter(
        Product.seller_id == current_user.id
    ).all()
    
    # Format response
    result = []
    for item in order_items:
        result.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "price": item.price,
            "order_id": item.order_id,
            "buyer_email": item.order.buyer.email,
            "order_status": item.order.status
        })
    
    return result
