# Database Architecture

This document explains how the e-commerce application interacts with the database.

## Database Schema

### Tables

**users**
- `id` - Primary key
- `email` - Unique user email
- `password_hash` - Bcrypt hashed password
- `role` - 'buyer' or 'seller'
- `created_at` - Timestamp

**products**
- `id` - Primary key
- `seller_id` - Foreign key to users
- `name` - Product name
- `description` - Product description
- `price` - Product price in Rupees
- `stock` - Available quantity
- `image_url` - Base64 encoded image or URL
- `created_at` - Timestamp

**orders**
- `id` - Primary key
- `buyer_id` - Foreign key to users
- `total_amount` - Order total in Rupees
- `status` - 'pending', 'processing', 'completed', or 'cancelled'
- `created_at` - Timestamp

**order_items**
- `id` - Primary key
- `order_id` - Foreign key to orders
- `product_id` - Foreign key to products
- `quantity` - Number of items
- `price` - Price at time of purchase

## Example: Creating a Product

### Frontend (JavaScript)
```javascript
// User uploads image and fills form
const productData = {
    name: "Wireless Headphones",
    description: "Premium noise-cancelling headphones",
    price: 12449.00,
    stock: 25,
    image_url: "data:image/jpeg;base64,..." // Base64 encoded
};

// Send to backend
await api.post('/api/products', productData);
```

### Backend (Python)
```python
# routes/product_routes.py
@router.post("/products")
def create_product(product_data: ProductCreate, current_user: User, db: Session):
    new_product = Product(
        seller_id=current_user.id,
        **product_data.dict()
    )
    db.add(new_product)
    db.commit()
    return new_product
```

### Database (SQL)
```sql
INSERT INTO products (seller_id, name, description, price, stock, image_url, created_at)
VALUES (2, 'Wireless Headphones', 'Premium noise-cancelling headphones', 
        12449.00, 25, 'data:image/jpeg;base64,...', '2026-01-04 00:00:00');
```

## Example: Placing an Order

### Frontend
```javascript
// Cart items
const orderData = {
    items: [
        { product_id: 1, quantity: 2 },
        { product_id: 2, quantity: 1 }
    ]
};

await api.post('/api/orders', orderData);
```

### Backend
```python
@router.post("/orders")
def create_order(order_data: OrderCreate, current_user: User, db: Session):
    # Calculate total and validate stock
    total = 0
    for item in order_data.items:
        product = db.query(Product).get(item.product_id)
        total += product.price * item.quantity
    
    # Create order
    order = Order(buyer_id=current_user.id, total_amount=total)
    db.add(order)
    db.commit()
    
    # Create order items and update stock
    for item in order_data.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )
        db.add(order_item)
        product.stock -= item.quantity
    
    db.commit()
    return order
```

## Technology Stack

- **Database**: SQLite (file: `ecommerce.db`)
- **ORM**: SQLAlchemy (Python ↔ SQL conversion)
- **Authentication**: JWT tokens + bcrypt password hashing
- **Image Storage**: Base64 encoding (stored as text)
- **Frontend Persistence**: localStorage for cart

## Database Location

- **Development**: `ecommerce.db` in project root
- **Production**: SQLite database on Render server

## Key Features

1. **Relationships**: SQLAlchemy automatically handles foreign keys
2. **Transactions**: All order operations are atomic (all or nothing)
3. **Stock Management**: Automatically decremented on order placement
4. **Price Locking**: Order items store price at time of purchase
5. **Image Storage**: Base64 encoding allows storing images in database

## Seeding Data

Run `python seed_data.py` to populate the database with:
- 2 test users (buyer and seller)
- 12 sample products

## Test Accounts

- **Buyer**: `buyer@aartipathak.com` / `buyer@123`
- **Seller**: `seller@aartipathak.com` / `seller@123`
