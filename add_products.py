from app import app, db, Product, Category
from datetime import datetime

def add_sample_data():
    # Clear existing data
    Product.query.delete()
    Category.query.delete()
    db.session.commit()

    # Create categories
    categories = [
        {
            'name': 'Laptops & Computers',
            'description': 'High-performance computers and accessories'
        },
        {
            'name': 'Smartphones & Tablets',
            'description': 'Mobile devices and accessories'
        },
        {
            'name': 'Audio & Headphones',
            'description': 'Premium audio equipment'
        },
        {
            'name': 'Gaming',
            'description': 'Gaming consoles and accessories'
        },
        {
            'name': 'Cameras & Photography',
            'description': 'Professional photography equipment'
        },
        {
            'name': 'Smart Home',
            'description': 'Smart home devices and automation'
        }
    ]

    # Add categories to database
    category_objects = {}
    for cat_data in categories:
        category = Category(**cat_data)
        db.session.add(category)
        db.session.flush()
        category_objects[cat_data['name']] = category

    # Sample products with categories
    products = [
        # Laptops & Computers
        {
            'name': 'Pro Gaming Laptop',
            'price': 1299.99,
            'description': 'High-performance gaming laptop with RTX 3070, 16GB RAM, 1TB SSD',
            'image_url': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=500',
            'category_id': category_objects['Laptops & Computers'].id,
            'stock': 50
        },
        {
            'name': 'Ultrabook Pro',
            'price': 999.99,
            'description': 'Ultra-thin laptop for professionals, 13" 4K display, 512GB SSD',
            'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500',
            'category_id': category_objects['Laptops & Computers'].id,
            'stock': 75
        },
        {
            'name': 'Desktop Workstation',
            'price': 1599.99,
            'description': 'Professional desktop computer with i9 processor and RTX 3080',
            'image_url': 'https://images.unsplash.com/photo-1547082299-de196ea013d6?w=500',
            'category_id': category_objects['Laptops & Computers'].id,
            'stock': 30
        },

        # Smartphones & Tablets
        {
            'name': 'Pro Smartphone',
            'price': 899.99,
            'description': 'Latest flagship smartphone with 108MP camera and 5G',
            'image_url': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500',
            'category_id': category_objects['Smartphones & Tablets'].id,
            'stock': 100
        },
        {
            'name': 'Tablet Pro 12.9',
            'price': 799.99,
            'description': '12.9-inch tablet with Retina display and stylus support',
            'image_url': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500',
            'category_id': category_objects['Smartphones & Tablets'].id,
            'stock': 60
        },
        {
            'name': 'Foldable Phone',
            'price': 1499.99,
            'description': 'Revolutionary foldable smartphone with dual display',
            'image_url': 'https://images.unsplash.com/photo-1578598336003-867ac56d90a2?w=500',
            'category_id': category_objects['Smartphones & Tablets'].id,
            'stock': 25
        },

        # Audio & Headphones
        {
            'name': 'Pro Wireless Headphones',
            'price': 299.99,
            'description': 'Premium noise-cancelling wireless headphones with 30-hour battery',
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500',
            'category_id': category_objects['Audio & Headphones'].id,
            'stock': 150
        },
        {
            'name': 'True Wireless Earbuds',
            'price': 159.99,
            'description': 'True wireless earbuds with active noise cancellation',
            'image_url': 'https://images.unsplash.com/photo-1606220838315-056192d5e927?w=500',
            'category_id': category_objects['Audio & Headphones'].id,
            'stock': 200
        },
        {
            'name': 'Studio Monitors',
            'price': 399.99,
            'description': 'Professional studio monitor speakers for audio production',
            'image_url': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?w=500',
            'category_id': category_objects['Audio & Headphones'].id,
            'stock': 40
        },

        # Gaming
        {
            'name': 'Pro Gaming Console',
            'price': 499.99,
            'description': 'Next-gen gaming console with 4K HDR gaming',
            'image_url': 'https://images.unsplash.com/photo-1486401899868-0e435ed85128?w=500',
            'category_id': category_objects['Gaming'].id,
            'stock': 80
        },
        {
            'name': 'VR Headset',
            'price': 399.99,
            'description': 'High-resolution VR headset with motion controllers',
            'image_url': 'https://images.unsplash.com/photo-1622979135225-d2ba269cf1ac?w=500',
            'category_id': category_objects['Gaming'].id,
            'stock': 45
        },
        {
            'name': 'Gaming Controller',
            'price': 59.99,
            'description': 'Professional gaming controller with customizable buttons',
            'image_url': 'https://images.unsplash.com/photo-1592840496694-26d035b52b48?w=500',
            'category_id': category_objects['Gaming'].id,
            'stock': 120
        },

        # Cameras & Photography
        {
            'name': 'Pro Mirrorless Camera',
            'price': 1999.99,
            'description': 'Professional mirrorless camera with 45MP sensor and 8K video',
            'image_url': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=500',
            'category_id': category_objects['Cameras & Photography'].id,
            'stock': 35
        },
        {
            'name': 'Vlogging Camera',
            'price': 749.99,
            'description': 'Compact camera perfect for vlogging and content creation',
            'image_url': 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=500',
            'category_id': category_objects['Cameras & Photography'].id,
            'stock': 55
        },
        {
            'name': 'Camera Lens',
            'price': 899.99,
            'description': 'Professional zoom lens for mirrorless cameras',
            'image_url': 'https://images.unsplash.com/photo-1495707902641-75cac588d2e9?w=500',
            'category_id': category_objects['Cameras & Photography'].id,
            'stock': 25
        },

        # Smart Home
        {
            'name': 'Smart Speaker',
            'price': 99.99,
            'description': 'Voice-controlled smart speaker with premium sound',
            'image_url': 'https://images.unsplash.com/photo-1589492477829-5e65395b66cc?w=500',
            'category_id': category_objects['Smart Home'].id,
            'stock': 150
        },
        {
            'name': 'Smart Display',
            'price': 149.99,
            'description': '10-inch smart display with voice control and video calling',
            'image_url': 'https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=500',
            'category_id': category_objects['Smart Home'].id,
            'stock': 70
        },
        {
            'name': 'Smart Security Camera',
            'price': 179.99,
            'description': 'HD security camera with night vision and two-way audio',
            'image_url': 'https://images.unsplash.com/photo-1557862921-37829c790f19?w=500',
            'category_id': category_objects['Smart Home'].id,
            'stock': 90
        }
    ]

    # Add products to database
    for product_data in products:
        product = Product(**product_data)
        db.session.add(product)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        add_sample_data()
        print("Sample categories and products have been added to the database!") 