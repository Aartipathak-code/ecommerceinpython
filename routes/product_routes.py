"""
Product management routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from database import get_db
from models import Product, User, UserRole
from auth import get_current_user, require_seller

router = APIRouter(prefix="/api/products", tags=["Products"])

# Pydantic models
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    image_url: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    seller_id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    image_url: Optional[str]
    
    class Config:
        from_attributes = True

@router.get("", response_model=List[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all products with optional filtering.
    
    Args:
        skip: Number of products to skip (pagination)
        limit: Maximum number of products to return
        search: Optional search term for product name
        db: Database session
        
    Returns:
        List of products
    """
    query = db.query(Product)
    
    if search:
        query = query.filter(Product.name.contains(search))
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a specific product by ID.
    
    Args:
        product_id: Product ID
        db: Database session
        
    Returns:
        Product object
        
    Raises:
        HTTPException: If product not found
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(require_seller),
    db: Session = Depends(get_db)
):
    """
    Create a new product (seller only).
    
    Args:
        product_data: Product creation data
        current_user: Current authenticated seller
        db: Database session
        
    Returns:
        Created product object
    """
    new_product = Product(
        seller_id=current_user.id,
        **product_data.dict()
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: User = Depends(require_seller),
    db: Session = Depends(get_db)
):
    """
    Update a product (seller only, own products only).
    
    Args:
        product_id: Product ID
        product_data: Product update data
        current_user: Current authenticated seller
        db: Database session
        
    Returns:
        Updated product object
        
    Raises:
        HTTPException: If product not found or not owned by seller
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if product.seller_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own products"
        )
    
    # Update only provided fields
    update_data = product_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    current_user: User = Depends(require_seller),
    db: Session = Depends(get_db)
):
    """
    Delete a product (seller only, own products only).
    
    Args:
        product_id: Product ID
        current_user: Current authenticated seller
        db: Database session
        
    Raises:
        HTTPException: If product not found or not owned by seller
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if product.seller_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own products"
        )
    
    db.delete(product)
    db.commit()
    
    return None

@router.get("/seller/my-products", response_model=List[ProductResponse])
def get_seller_products(
    current_user: User = Depends(require_seller),
    db: Session = Depends(get_db)
):
    """
    Get all products for the current seller.
    
    Args:
        current_user: Current authenticated seller
        db: Database session
        
    Returns:
        List of seller's products
    """
    products = db.query(Product).filter(Product.seller_id == current_user.id).all()
    return products
