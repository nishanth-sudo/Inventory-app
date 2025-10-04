from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from datetime import datetime
import os
import uuid

# Import database models
from db import db, User, Product, Location, ProductMovement

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-for-testing-12345'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF globally for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'basic'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
    class Meta:
        csrf = False  # Temporarily disable CSRF for testing

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')
    
    class Meta:
        csrf = False  # Temporarily disable CSRF for testing

class ProductForm(FlaskForm):
    product_id = StringField('Product ID', validators=[DataRequired(), Length(min=1, max=50)])
    name = StringField('Product Name', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description')
    submit = SubmitField('Save Product')

class LocationForm(FlaskForm):
    location_id = StringField('Location ID', validators=[DataRequired(), Length(min=1, max=50)])
    name = StringField('Location Name', validators=[DataRequired(), Length(min=1, max=100)])
    address = TextAreaField('Address')
    submit = SubmitField('Save Location')

class MovementForm(FlaskForm):
    movement_id = StringField('Movement ID', validators=[DataRequired(), Length(min=1, max=50)])
    from_location = SelectField('From Location', choices=[], coerce=str)
    to_location = SelectField('To Location', choices=[], coerce=str)
    product_id = SelectField('Product', validators=[DataRequired()], coerce=str)
    qty = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Save Movement')

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    print(f"Form submitted: {request.method == 'POST'}")
    print(f"Form validation: {form.validate_on_submit()}")
    if form.errors:
        print(f"Form errors: {form.errors}")
    
    if form.validate_on_submit():
        print(f"Username: {form.username.data}")
        user = User.query.filter_by(username=form.username.data).first()
        print(f"User found: {user is not None}")
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Invalid username or password', 'error')
    
    return render_template('login.html', form=form)

@app.route('/test-user')
def test_user():
    """Test route to check if admin user exists"""
    admin_user = User.query.filter_by(username='admin').first()
    if admin_user:
        return f"Admin user exists: {admin_user.username}, {admin_user.email}"
    else:
        return "Admin user not found!"

@app.route('/test-login')
def test_login():
    """Test route to manually login admin user"""
    admin_user = User.query.filter_by(username='admin').first()
    if admin_user:
        result = login_user(admin_user)
        print(f"Login result: {result}")
        print(f"Current user authenticated: {current_user.is_authenticated}")
        print(f"Current user: {current_user}")
        flash('Test login successful!', 'success')
        return redirect(url_for('index'))
    else:
        return "Admin user not found!"

@app.route('/test-session')
def test_session():
    """Test session and authentication status"""
    return f"""
    <h2>Session Test</h2>
    <p>Current user authenticated: {current_user.is_authenticated}</p>
    <p>Current user: {current_user}</p>
    <p>Session: {dict(session)}</p>
    <p><a href="/test-login">Test Login</a></p>
    <p><a href="/login">Regular Login</a></p>
    <p><a href="/">Home</a></p>
    """

@app.route('/test-add-product')
@login_required  
def test_add_product():
    """Test route to add a product without forms"""
    try:
        test_product = Product(
            product_id='TEST-001',
            name='Test Product',
            description='This is a test product created via test route'
        )
        db.session.add(test_product)
        db.session.commit()
        return "Test product added successfully! <a href='/products'>View Products</a>"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/debug-form', methods=['GET', 'POST'])
@login_required
def debug_form():
    """Simple debug form to test form submissions"""
    if request.method == 'POST':
        return f"Form submitted! Data: {dict(request.form)}"
    
    return '''
    <h2>Debug Form Test</h2>
    <form method="POST">
        <input type="text" name="test_field" placeholder="Enter something" required>
        <button type="submit">Submit</button>
    </form>
    <p><a href="/products/add">Go to Add Product</a></p>
    '''

@app.route('/debug-auth')
def debug_auth():
    """Debug authentication status"""
    return f"""
    <h2>Authentication Debug</h2>
    <p>Current user authenticated: {current_user.is_authenticated}</p>
    <p>Current user: {current_user}</p>
    <p>Session: {dict(session)}</p>
    <p><a href="/login">Login</a></p>
    <p><a href="/test-login">Test Login</a></p>
    <p><a href="/products/add">Add Product</a></p>
    """

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'error')
            return render_template('register.html', form=form)
        
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
@app.route('/')
@login_required
def index():
    # Dashboard with quick stats
    total_products = Product.query.count()
    total_locations = Location.query.count()
    total_movements = ProductMovement.query.count()
    
    # Recent movements
    recent_movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).limit(5).all()
    
    return render_template('index.html', 
                         total_products=total_products,
                         total_locations=total_locations,
                         total_movements=total_movements,
                         recent_movements=recent_movements)

# Product routes
@app.route('/products')
@login_required
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    print(f"Add Product - Method: {request.method}")
    if request.method == 'POST':
        print(f"Form data: {request.form}")
        try:
            product_id = request.form['product_id']
            name = request.form['name']
            description = request.form['description']
            
            print(f"Creating product: ID={product_id}, Name={name}")
            
            if Product.query.get(product_id):
                flash('Product ID already exists!', 'error')
                return redirect(url_for('add_product'))
            
            product = Product(product_id=product_id, name=name, description=description)
            db.session.add(product)
            db.session.commit()
            print("Product added successfully to database")
            flash('Product added successfully!', 'success')
            return redirect(url_for('products'))
        except Exception as e:
            print(f"Error adding product: {e}")
            flash(f'Error adding product: {str(e)}', 'error')
            return redirect(url_for('add_product'))
    
    return render_template('add_product.html')

@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('edit_product.html', product=product)

@app.route('/products/delete/<product_id>')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products'))

# Location routes
@app.route('/locations')
@login_required
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/locations/add', methods=['GET', 'POST'])
@login_required
def add_location():
    if request.method == 'POST':
        location_id = request.form['location_id']
        name = request.form['name']
        address = request.form['address']
        
        if Location.query.get(location_id):
            flash('Location ID already exists!', 'error')
            return redirect(url_for('add_location'))
        
        location = Location(location_id=location_id, name=name, address=address)
        db.session.add(location)
        db.session.commit()
        flash('Location added successfully!', 'success')
        return redirect(url_for('locations'))
    
    return render_template('add_location.html')

@app.route('/locations/edit/<location_id>', methods=['GET', 'POST'])
@login_required
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    
    if request.method == 'POST':
        location.name = request.form['name']
        location.address = request.form['address']
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('locations'))
    
    return render_template('edit_location.html', location=location)

@app.route('/locations/delete/<location_id>')
@login_required
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted successfully!', 'success')
    return redirect(url_for('locations'))

# Movement routes
@app.route('/movements')
@login_required
def movements():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements.html', movements=movements)

@app.route('/movements/add', methods=['GET', 'POST'])
@login_required
def add_movement():
    if request.method == 'POST':
        movement_id = request.form['movement_id']
        from_location = request.form['from_location'] if request.form['from_location'] else None
        to_location = request.form['to_location'] if request.form['to_location'] else None
        product_id = request.form['product_id']
        qty = int(request.form['qty'])
        
        if ProductMovement.query.get(movement_id):
            flash('Movement ID already exists!', 'error')
            return redirect(url_for('add_movement'))
        
        if not from_location and not to_location:
            flash('Either from_location or to_location must be specified!', 'error')
            return redirect(url_for('add_movement'))
        
        if from_location == to_location:
            flash('From location and to location cannot be the same!', 'error')
            return redirect(url_for('add_movement'))
        
        movement = ProductMovement(
            movement_id=movement_id,
            from_location=from_location,
            to_location=to_location,
            product_id=product_id,
            qty=qty
        )
        
        # Validate movement
        is_valid, message = movement.validate_movement()
        if not is_valid:
            flash(message, 'error')
            return redirect(url_for('add_movement'))
        
        db.session.add(movement)
        db.session.commit()
        
        # Update product total quantity
        product = Product.query.get(product_id)
        if product:
            product.update_total_qty()
        
        flash('Movement added successfully!', 'success')
        return redirect(url_for('movements'))
    
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('add_movement.html', products=products, locations=locations)

@app.route('/movements/edit/<movement_id>', methods=['GET', 'POST'])
@login_required
def edit_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    
    if request.method == 'POST':
        movement.from_location = request.form['from_location'] if request.form['from_location'] else None
        movement.to_location = request.form['to_location'] if request.form['to_location'] else None
        movement.product_id = request.form['product_id']
        movement.qty = int(request.form['qty'])
        
        if not movement.from_location and not movement.to_location:
            flash('Either from_location or to_location must be specified!', 'error')
            return redirect(url_for('edit_movement', movement_id=movement_id))
        
        if movement.from_location == movement.to_location:
            flash('From location and to location cannot be the same!', 'error')
            return redirect(url_for('edit_movement', movement_id=movement_id))
        
        db.session.commit()
        flash('Movement updated successfully!', 'success')
        return redirect(url_for('movements'))
    
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('edit_movement.html', movement=movement, products=products, locations=locations)

@app.route('/movements/delete/<movement_id>')
@login_required
def delete_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    db.session.delete(movement)
    db.session.commit()
    flash('Movement deleted successfully!', 'success')
    return redirect(url_for('movements'))

# Balance Report
@app.route('/balance')
@login_required
def balance():
    # Get all products and locations
    products = Product.query.all()
    locations = Location.query.all()
    
    # Calculate balance for each product-location combination
    balance_data = []
    
    for product in products:
        for location in locations:
            # Calculate total in (to_location)
            total_in = db.session.query(db.func.sum(ProductMovement.qty)).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.to_location == location.location_id
            ).scalar() or 0
            
            # Calculate total out (from_location)
            total_out = db.session.query(db.func.sum(ProductMovement.qty)).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.from_location == location.location_id
            ).scalar() or 0
            
            balance = total_in - total_out
            
            if balance > 0:  # Only show locations with positive balance
                balance_data.append({
                    'product': product.name,
                    'location': location.name,
                    'qty': balance
                })
    
    return render_template('balance.html', balance_data=balance_data)

def init_sample_data():
    """Initialize sample data if database is empty"""
    
    # Check if data already exists
    if User.query.count() > 0:
        return
    
    # Create default admin user
    admin_user = User(username='admin', email='admin@example.com')
    admin_user.set_password('admin123')
    db.session.add(admin_user)
    
    # Create sample products
    products = [
        Product(product_id='LAPTOP-001', name='Laptop', description='High-performance laptop for office use'),
        Product(product_id='MOUSE-001', name='Mouse', description='Wireless optical mouse'),
        Product(product_id='KEYBOARD-001', name='Keyboard', description='Mechanical keyboard with backlight'),
        Product(product_id='MONITOR-001', name='Monitor', description='24-inch LED monitor')
    ]
    
    for product in products:
        db.session.add(product)
    
    # Create sample locations
    locations = [
        Location(location_id='WH-A', name='Warehouse A', address='123 Industrial District, City Center'),
        Location(location_id='WH-B', name='Warehouse B', address='456 Storage Avenue, Business Park'),
        Location(location_id='STORE-1', name='Store Front', address='789 Main Street, Downtown'),
        Location(location_id='OFFICE-1', name='Office', address='321 Corporate Plaza, Financial District')
    ]
    
    for location in locations:
        db.session.add(location)
    
    # Commit products and locations first
    db.session.commit()
    
    # Create sample movements
    movements = [
        # Initial stock - Inbound movements (External -> Warehouse A)
        ProductMovement(movement_id='MOV-001', from_location=None, to_location='WH-A', product_id='LAPTOP-001', qty=50),
        ProductMovement(movement_id='MOV-002', from_location=None, to_location='WH-A', product_id='MOUSE-001', qty=100),
        ProductMovement(movement_id='MOV-003', from_location=None, to_location='WH-A', product_id='KEYBOARD-001', qty=75),
        ProductMovement(movement_id='MOV-004', from_location=None, to_location='WH-A', product_id='MONITOR-001', qty=30),
        
        # Transfer to Warehouse B
        ProductMovement(movement_id='MOV-005', from_location='WH-A', to_location='WH-B', product_id='LAPTOP-001', qty=20),
        ProductMovement(movement_id='MOV-006', from_location='WH-A', to_location='WH-B', product_id='MOUSE-001', qty=40),
        ProductMovement(movement_id='MOV-007', from_location='WH-A', to_location='WH-B', product_id='KEYBOARD-001', qty=30),
        ProductMovement(movement_id='MOV-008', from_location='WH-A', to_location='WH-B', product_id='MONITOR-001', qty=15),
        
        # Transfer to Store Front
        ProductMovement(movement_id='MOV-009', from_location='WH-A', to_location='STORE-1', product_id='LAPTOP-001', qty=15),
        ProductMovement(movement_id='MOV-010', from_location='WH-A', to_location='STORE-1', product_id='MOUSE-001', qty=25),
        ProductMovement(movement_id='MOV-011', from_location='WH-B', to_location='STORE-1', product_id='KEYBOARD-001', qty=10),
        ProductMovement(movement_id='MOV-012', from_location='WH-B', to_location='STORE-1', product_id='MONITOR-001', qty=8),
        
        # Transfer to Office
        ProductMovement(movement_id='MOV-013', from_location='WH-A', to_location='OFFICE-1', product_id='LAPTOP-001', qty=5),
        ProductMovement(movement_id='MOV-014', from_location='WH-B', to_location='OFFICE-1', product_id='MOUSE-001', qty=10),
        ProductMovement(movement_id='MOV-015', from_location='STORE-1', to_location='OFFICE-1', product_id='KEYBOARD-001', qty=3),
        
        # Some outbound movements (Sales - Location -> External)
        ProductMovement(movement_id='MOV-016', from_location='STORE-1', to_location=None, product_id='LAPTOP-001', qty=8),
        ProductMovement(movement_id='MOV-017', from_location='STORE-1', to_location=None, product_id='MOUSE-001', qty=15),
        ProductMovement(movement_id='MOV-018', from_location='STORE-1', to_location=None, product_id='KEYBOARD-001', qty=5),
        ProductMovement(movement_id='MOV-019', from_location='STORE-1', to_location=None, product_id='MONITOR-001', qty=3),
        
        # Additional stock replenishment
        ProductMovement(movement_id='MOV-020', from_location=None, to_location='WH-B', product_id='LAPTOP-001', qty=25),
        ProductMovement(movement_id='MOV-021', from_location=None, to_location='WH-A', product_id='MOUSE-001', qty=50),
    ]
    
    for movement in movements:
        db.session.add(movement)
    
    # Commit all movements
    db.session.commit()
    
    # Update total quantities for all products
    for product in products:
        product.update_total_qty()
    
    db.session.commit()
    print("Sample data initialized successfully!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_sample_data()
    app.run(debug=True)

