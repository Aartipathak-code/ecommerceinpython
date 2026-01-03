# E-Commerce Platform

A full-stack e-commerce application built with Python (FastAPI) backend and vanilla JavaScript frontend. Buyers can browse and purchase products, while sellers can list and manage their inventory.

## Features

### For Buyers
- 🛍️ Browse products with search functionality
- 🛒 Shopping cart with real-time updates
- 📦 Place orders and view order history
- 🔐 Secure authentication with JWT

### For Sellers
- 📝 List and manage products (CRUD operations)
- 📊 View orders for your products
- 💰 Track sales and inventory
- 🖼️ Add product images via URL

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **JWT**: Secure token-based authentication
- **Bcrypt**: Password hashing

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **Modern CSS**: Dark theme with glassmorphism effects
- **Responsive Design**: Works on all devices

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd c:\Users\91930\ecommerceinpython
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Open your browser**
   Navigate to: http://localhost:8000

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

#### Products
- `GET /api/products` - List all products (with optional search)
- `GET /api/products/{id}` - Get product details
- `POST /api/products` - Create product (seller only)
- `PUT /api/products/{id}` - Update product (seller only)
- `DELETE /api/products/{id}` - Delete product (seller only)
- `GET /api/products/seller/my-products` - Get seller's products

#### Orders
- `POST /api/orders` - Create order (buyer only)
- `GET /api/orders` - Get user's orders (buyer only)
- `GET /api/orders/{id}` - Get order details
- `GET /api/orders/seller/orders` - Get seller's orders

## Usage Guide

### As a Buyer

1. **Register**: Click "Register" and select "Buy Products"
2. **Browse**: View all available products on the home page
3. **Search**: Use the search box to find specific products
4. **Add to Cart**: Click "Add to Cart" on products you want
5. **Checkout**: Open cart and click "Checkout" to place order
6. **View Orders**: Navigate to "My Orders" to see order history

### As a Seller

1. **Register**: Click "Register" and select "Sell Products"
2. **Add Products**: Go to "Seller Dashboard" and click "Add Product"
3. **Manage Products**: Edit or delete your products from the dashboard
4. **View Orders**: Check the "Orders" tab to see purchases of your products

## Project Structure

```
ecommerceinpython/
├── main.py                 # FastAPI application entry point
├── database.py             # Database configuration
├── models.py               # SQLAlchemy models
├── auth.py                 # Authentication utilities
├── routes/                 # API route handlers
│   ├── auth_routes.py
│   ├── product_routes.py
│   └── order_routes.py
├── static/                 # Frontend files
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js
│       ├── auth.js
│       ├── products.js
│       ├── cart.js
│       └── orders.js
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Database Schema

### Users
- id, email, password_hash, role (buyer/seller), created_at

### Products
- id, seller_id, name, description, price, stock, image_url, created_at

### Orders
- id, buyer_id, total_amount, status, created_at

### OrderItems
- id, order_id, product_id, quantity, price

## Security Notes

⚠️ **Important**: This is a demonstration project. For production use:
- Change the `SECRET_KEY` in `auth.py`
- Use environment variables for sensitive data
- Use HTTPS in production
- Implement rate limiting
- Add input validation and sanitization
- Use a production database (PostgreSQL, MySQL)
- Implement proper error handling

## Development

### Running Tests
```bash
pytest test_api.py -v
```

### Database Reset
To reset the database, simply delete `ecommerce.db` and restart the application.

## License

This project is for educational purposes.

## Support

For issues or questions, please check the API documentation at http://localhost:8000/docs
