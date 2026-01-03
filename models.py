"""
Database models for the e-commerce application.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class UserRole(str, enum.Enum):
    """User role enumeration."""
    BUYER = "buyer"
    SELLER = "seller"

class OrderStatus(str, enum.Enum):
    """Order status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class User(Base):
    """User model for both buyers and sellers."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    products = relationship("Product", back_populates="seller", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="buyer", cascade="all, delete-orphan")

class Product(Base):
    """Product model for items listed by sellers."""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    image_url = Column(Text)  # Changed to Text to support Base64 encoded images
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    seller = relationship("User", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    """Order model for buyer purchases."""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    buyer = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    """Order item model for individual products in an order."""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # Price at time of purchase
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
