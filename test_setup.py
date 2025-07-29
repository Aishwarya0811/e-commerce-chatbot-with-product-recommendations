#!/usr/bin/env python3
"""
Simple test script to verify the application setup
"""

import sys
import os
from database import create_tables, seed_database, SessionLocal, Product

def test_database():
    """Test database creation and seeding"""
    print("🔍 Testing database setup...")
    
    try:
        # Create tables
        create_tables()
        print("✅ Database tables created successfully")
        
        # Seed database
        seed_database()
        print("✅ Database seeded successfully")
        
        # Verify products exist
        db = SessionLocal()
        products = db.query(Product).all()
        db.close()
        
        print(f"✅ Found {len(products)} products in database:")
        for product in products:
            print(f"   - {product.name} ({product.category}) - ${product.price}")
            
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("\n🔍 Testing environment setup...")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key or openai_key == "your-openai-api-key-here":
        print("⚠️  OpenAI API key not configured")
        print("   Please update the .env file with your actual API key")
        return False
    else:
        print("✅ OpenAI API key configured")
        return True

def test_dependencies():
    """Test required dependencies"""
    print("\n🔍 Testing dependencies...")
    
    required_modules = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'openai',
        'python_dotenv',
        'pydantic'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} is installed")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ {module} is missing")
    
    if missing_modules:
        print(f"\n❌ Missing dependencies: {', '.join(missing_modules)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_static_files():
    """Test static files exist"""
    print("\n🔍 Testing static files...")
    
    static_files = [
        'static/index.html',
        'static/style.css',
        'static/script.js'
    ]
    
    missing_files = []
    
    for file_path in static_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path} is missing")
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 E-commerce Chatbot Setup Test\n")
    
    tests = [
        test_dependencies,
        test_database,
        test_static_files,
        test_environment
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*50)
    
    if all(results):
        print("🎉 All tests passed! Your application is ready to run.")
        print("\nTo start the application:")
        print("   python main.py")
        print("\nThen visit: http://localhost:8000")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()