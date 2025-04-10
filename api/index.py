from app import app

# Initialize the database
with app.app_context():
    from app import db
    db.create_all() 