"""
Main FastAPI application for the e-commerce platform.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes import auth_routes, product_routes, order_routes

# Create FastAPI app
app = FastAPI(
    title="E-Commerce API",
    description="A full-stack e-commerce platform with buyer and seller capabilities",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router)
app.include_router(product_routes.router)
app.include_router(order_routes.router)

# Mount static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_db()
    print("Database initialized successfully!")
    
    # Seed database with initial data
    try:
        from seed_data import seed_database
        seed_database()
    except Exception as e:
        print(f"Note: Database seeding skipped or failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
