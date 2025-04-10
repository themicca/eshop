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
    
    # Add products
    products = [
        Product(
            name='Laptop',
            description='High-performance laptop with latest specs',
            price=999.99,
            stock=10,
            category=electronics
        ),
        Product(
            name='Smartphone',
            description='Latest model smartphone with great camera',
            price=699.99,
            stock=15,
            category=electronics
        ),
        Product(
            name='T-Shirt',
            description='Comfortable cotton t-shirt',
            price=19.99,
            stock=50,
            category=clothing
        ),
        Product(
            name='Jeans',
            description='Classic blue jeans',
            price=49.99,
            stock=30,
            category=clothing
        ),
        Product(
            name='Python Programming',
            description='Comprehensive guide to Python',
            price=29.99,
            stock=20,
            category=books
        ),
        Product(
            name='Web Development',
            description='Modern web development techniques',
            price=34.99,
            stock=25,
            category=books
        )
    ]
    
    db.session.add_all(products)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        add_sample_data()
        print("Sample categories and products have been added to the database!") 