from app import app, db, Product, Category
from datetime import datetime

def add_sample_data():
    # Clear existing data
    Product.query.delete()
    Category.query.delete()
    db.session.commit()

    # Add categories
    electronics = Category(name='Electronics')
    clothing = Category(name='Clothing')
    books = Category(name='Books')
    
    db.session.add_all([electronics, clothing, books])
    db.session.commit()
    
    # Add products with proper image URLs
    products = [
        Product(
            name='Laptop',
            description='High-performance laptop with latest specs',
            price=999.99,
            stock=10,
            category=electronics,
            image_url='https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500'
        ),
        Product(
            name='Smartphone',
            description='Latest model smartphone with great camera',
            price=699.99,
            stock=15,
            category=electronics,
            image_url='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500'
        ),
        Product(
            name='T-Shirt',
            description='Comfortable cotton t-shirt',
            price=19.99,
            stock=50,
            category=clothing,
            image_url='https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500'
        ),
        Product(
            name='Jeans',
            description='Classic blue jeans',
            price=49.99,
            stock=30,
            category=clothing,
            image_url='https://images.unsplash.com/photo-1542272454315-4c01d7abdf4a?w=500'
        ),
        Product(
            name='Python Programming',
            description='Comprehensive guide to Python',
            price=29.99,
            stock=20,
            category=books,
            image_url='https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=500'
        ),
        Product(
            name='Web Development',
            description='Modern web development techniques',
            price=34.99,
            stock=25,
            category=books,
            image_url='https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?w=500'
        )
    ]
    
    db.session.add_all(products)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        add_sample_data()
        print("Sample categories and products have been added to the database!") 