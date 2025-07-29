from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLITE_DATABASE_URL = "sqlite:///./ecommerce.db"

engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    category = Column(String, index=True)
    price = Column(Float)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_database():
    db = SessionLocal()
    
    # Check if products already exist
    if db.query(Product).first():
        db.close()
        return
    
    # Seed data
    products = [
        Product(name="Wireless Headphones", description="High-quality Bluetooth headphones with noise cancellation", category="Electronics", price=199.99),
        Product(name="Smartphone", description="Latest model with advanced camera and fast processor", category="Electronics", price=699.99),
        Product(name="Yoga Mat", description="Non-slip exercise mat perfect for yoga and fitness", category="Fitness", price=29.99),
        Product(name="Resistance Bands Set", description="Complete set of resistance bands for strength training", category="Fitness", price=24.99),
        Product(name="Coffee Maker", description="Programmable coffee maker with 12-cup capacity", category="Home", price=89.99),
        Product(name="Air Purifier", description="HEPA filter air purifier for clean indoor air", category="Home", price=149.99)
    ]
    
    db.add_all(products)
    db.commit()
    db.close()