from flask import Flask
from app import app, db, Category, Product
from add_products import add_sample_data

# Initialize database and add sample data for each request
@app.before_request
def init_db():
    db.create_all()
    # Only add sample data if there are no categories
    if not Category.query.first():
        try:
            add_sample_data()
        except Exception as e:
            print(f"Error adding sample data: {e}")

# This is required for Vercel
app.debug = False

# This is the main entry point for Vercel
app = app 