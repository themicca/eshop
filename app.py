from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///eshop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# This is for Vercel
app.debug = False

# Models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    stock = db.Column(db.Integer, default=100)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    cart_items = db.relationship('CartItem', backref='user', lazy=True)
    # Add fields for user details
    full_name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    phone = db.Column(db.String(20))

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    # Shipping information
    shipping_address = db.Column(db.String(200))
    shipping_city = db.Column(db.String(100))
    shipping_country = db.Column(db.String(100))
    shipping_postal_code = db.Column(db.String(20))
    # Payment information (in practice, you'd want to use a payment processor)
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(20))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    sort = request.args.get('sort', 'name')
    
    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.name.asc())
    
    products = query.paginate(page=page, per_page=9, error_out=False)
    categories = Category.query.all()
    return render_template('index.html', products=products, categories=categories)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Here you would typically process the contact form
        flash('Thank you for your message. We will get back to you soon!')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/category/<int:category_id>')
def category(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template('category.html', category=category, products=products)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty')
        return redirect(url_for('cart'))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    if request.method == 'POST':
        # Validate required fields
        required_fields = ['full_name', 'address', 'city', 'postal_code', 'country', 'phone',
                         'card_name', 'card_number', 'expiry', 'cvv']
        for field in required_fields:
            if not request.form.get(field):
                flash(f'{field.replace("_", " ").title()} is required')
                return redirect(url_for('checkout'))
        
        # Calculate final total with shipping
        shipping_method = request.form.get('shipping_method', 'standard')
        if shipping_method == 'express':
            shipping_cost = 19.99
        elif total <= 50:
            shipping_cost = 9.99
        else:
            shipping_cost = 0
            
        final_total = total + shipping_cost
        
        # Update user details
        current_user.full_name = request.form.get('full_name')
        current_user.address = request.form.get('address')
        current_user.city = request.form.get('city')
        current_user.postal_code = request.form.get('postal_code')
        current_user.country = request.form.get('country')
        current_user.phone = request.form.get('phone')
        
        # Create new order
        order = Order(
            user_id=current_user.id,
            order_date=datetime.now(timezone.utc),
            total_amount=final_total,
            status='pending',
            shipping_address=request.form.get('address'),
            shipping_city=request.form.get('city'),
            shipping_country=request.form.get('country'),
            shipping_postal_code=request.form.get('postal_code'),
            payment_method='credit_card',
            payment_status='paid'
        )
        db.session.add(order)
        
        # Clear cart
        for item in cart_items:
            db.session.delete(item)
        
        db.session.commit()
        flash('Order placed successfully!')
        return redirect(url_for('index'))
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Update user settings
        current_user.full_name = request.form.get('full_name')
        current_user.address = request.form.get('address')
        current_user.city = request.form.get('city')
        current_user.postal_code = request.form.get('postal_code')
        current_user.country = request.form.get('country')
        current_user.phone = request.form.get('phone')
        
        # Only update password if provided
        new_password = request.form.get('new_password')
        if new_password:
            current_user.password_hash = generate_password_hash(new_password)
        
        db.session.commit()
        flash('Settings updated successfully!')
        return redirect(url_for('settings'))
    
    return render_template('settings.html')

@app.route('/my_orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).all()
    return render_template('my_orders.html', orders=orders)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id)
        db.session.add(cart_item)
    
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    if cart_item.user_id == current_user.id:
        db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for('cart'))

@app.route('/update_cart_quantity/<int:cart_item_id>', methods=['POST'])
@login_required
def update_cart_quantity(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    if cart_item.user_id != current_user.id:
        flash('Unauthorized action')
        return redirect(url_for('cart'))
    
    quantity = request.form.get('quantity', type=int)
    if quantity is not None and quantity > 0:
        cart_item.quantity = quantity
        db.session.commit()
    
    return redirect(url_for('cart'))

# Remove the if __name__ == '__main__' block since Vercel will handle the server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8080) 