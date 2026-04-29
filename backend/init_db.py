from database import engine, Base, SessionLocal, get_db
from models import Site, User, PageView, Event, Session
from utils import generate_site_key, generate_api_key
from auth import get_password_hash
from sqlalchemy.orm import Session


def init_database():
    """Initialize the database with tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def create_default_user_and_site():
    """Create default user and sample site"""
    db = SessionLocal()
    try:
        # Check if default user already exists
        existing_user = db.query(User).filter(User.email == "admin@example.com").first()
        if existing_user:
            print("Default user already exists.")
            user = existing_user
        else:
            # Create default user
            user = User(
                email="admin@example.com",
                password_hash=get_password_hash("admin123")
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print("Default user created:")
            print(f"  Email: admin@example.com")
            print(f"  Password: admin123")
        
        # Check if sample site already exists
        existing_site = db.query(Site).filter(Site.domain == "example.com").first()
        if existing_site:
            print("Sample site already exists.")
        else:
            # Create sample site
            site = Site(
                name="Example Website",
                domain="example.com",
                site_key=generate_site_key(),
                api_key=generate_api_key(),
                owner_id=user.id
            )
            db.add(site)
            db.commit()
            db.refresh(site)
            
            print(f"Sample site created:")
            print(f"  Name: {site.name}")
            print(f"  Domain: {site.domain}")
            print(f"  Site Key: {site.site_key}")
            print(f"  API Key: {site.api_key}")
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
    create_default_user_and_site()
