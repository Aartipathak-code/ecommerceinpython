"""
Seed script to populate the database with sample data for testing.
"""
from database import SessionLocal
from models import User, Product, UserRole
from auth import hash_password

def seed_database():
    """Add sample users and products to the database."""
    db = SessionLocal()
    
    try:
        # Check if products already exist
        existing_products = db.query(Product).count()
        if existing_products > 0:
            print(f"Database already has {existing_products} products. Skipping seed.")
            return
        
        # Check if users exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"Found {existing_users} existing users. Will add products only.")
            # Get existing sellers
            sellers = db.query(User).filter(User.role == UserRole.SELLER).all()
            if len(sellers) < 2:
                print("Not enough sellers found. Please ensure at least 2 seller accounts exist.")
                return
            seller1 = sellers[0]
            seller2 = sellers[1] if len(sellers) > 1 else sellers[0]
        else:
            # Create sample users
            print("Creating sample users...")
            
            # Buyer account
            buyer = User(
                email="buyer@aartipathak.com",
                password_hash=hash_password("buyer@123"),
                role=UserRole.BUYER
            )
            db.add(buyer)
            
            # Seller account
            seller1 = User(
                email="seller@aartipathak.com",
                password_hash=hash_password("seller@123"),
                role=UserRole.SELLER
            )
            db.add(seller1)
            
            db.commit()
            db.refresh(seller1)
            seller2 = seller1  # Use same seller for all products
            
            print(f"[OK] Created users: buyer@aartipathak.com (buyer), seller@aartipathak.com (seller)")
        
        # Create sample products
        print("Creating sample products...")
        
        products = [
            # Electronics
            Product(
                seller_id=seller1.id,
                name="Wireless Headphones",
                description="Premium noise-cancelling wireless headphones with 30-hour battery life",
                price=12449.00,
                stock=25,
                image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"
            ),
            Product(
                seller_id=seller1.id,
                name="Smart Watch",
                description="Fitness tracker with heart rate monitor and GPS",
                price=24899.00,
                stock=15,
                image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"
            ),
            Product(
                seller_id=seller1.id,
                name="Laptop Stand",
                description="Ergonomic aluminum laptop stand for better posture",
                price=4149.00,
                stock=50,
                image_url="https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500"
            ),
            Product(
                seller_id=seller2.id,
                name="Mechanical Keyboard",
                description="RGB backlit mechanical keyboard with blue switches",
                price=10799.00,
                stock=30,
                image_url="https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500"
            ),
            Product(
                seller_id=seller2.id,
                name="Wireless Mouse",
                description="Ergonomic wireless mouse with precision tracking",
                price=3319.00,
                stock=40,
                image_url="https://images.unsplash.com/photo-1527814050087-3793815479db?w=500"
            ),
            # Home & Living
            Product(
                seller_id=seller1.id,
                name="Coffee Maker",
                description="Programmable coffee maker with thermal carafe",
                price=6639.00,
                stock=20,
                image_url="https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=500"
            ),
            Product(
                seller_id=seller2.id,
                name="Desk Lamp",
                description="LED desk lamp with adjustable brightness and color temperature",
                price=2904.00,
                stock=35,
                image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500"
            ),
            Product(
                seller_id=seller1.id,
                name="Water Bottle",
                description="Insulated stainless steel water bottle, keeps drinks cold for 24 hours",
                price=2074.00,
                stock=60,
                image_url="https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"
            ),
            # Fashion
            Product(
                seller_id=seller2.id,
                name="Backpack",
                description="Durable travel backpack with laptop compartment",
                price=4979.00,
                stock=45,
                image_url="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500"
            ),
            Product(
                seller_id=seller1.id,
                name="Sunglasses",
                description="Polarized UV protection sunglasses",
                price=7469.00,
                stock=28,
                image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500"
            ),
            # Sports & Fitness
            Product(
                seller_id=seller2.id,
                name="Yoga Mat",
                description="Non-slip yoga mat with carrying strap",
                price=2489.00,
                stock=55,
                image_url="https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500"
            ),
            Product(
                seller_id=seller1.id,
                name="Resistance Bands Set",
                description="Set of 5 resistance bands for strength training",
                price=1659.00,
                stock=70,
                image_url="https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=500"
            ),
        ]
        
        for product in products:
            db.add(product)
        
        db.commit()
        print(f"[OK] Created {len(products)} sample products")
        
        print("\n" + "="*60)
        print("Database seeded successfully!")
        print("="*60)
        print("\nTest Accounts:")
        print("  Buyer:  buyer@aartipathak.com / buyer@123")
        print("  Seller: seller@aartipathak.com / seller@123")
        print("\nYou can now test the application with these accounts.")
        print("="*60)
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
