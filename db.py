"""
Database models for Inventory Management System
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Product(db.Model):
    """Product model for inventory items"""
    product_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    total_qty = db.Column(db.Integer, default=0, nullable=False)
    
    def get_current_stock(self):
        """Calculate current total stock from movements"""
        # Inbound movements (to any location from external)
        inbound = db.session.query(db.func.sum(ProductMovement.qty)).filter(
            ProductMovement.product_id == self.product_id,
            ProductMovement.from_location == None,
            ProductMovement.to_location != None
        ).scalar() or 0
        
        # Outbound movements (from any location to external)
        outbound = db.session.query(db.func.sum(ProductMovement.qty)).filter(
            ProductMovement.product_id == self.product_id,
            ProductMovement.from_location != None,
            ProductMovement.to_location == None
        ).scalar() or 0
        
        return inbound - outbound
    
    def update_total_qty(self):
        """Update total_qty based on movements"""
        self.total_qty = self.get_current_stock()
        db.session.commit()
    
    def __repr__(self):
        return f'<Product {self.product_id}: {self.name}>'


class Location(db.Model):
    """Location model for warehouse/storage locations"""
    location_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    
    def get_product_qty(self, product_id):
        """Get quantity of a specific product at this location"""
        # Total received at this location
        total_in = db.session.query(db.func.sum(ProductMovement.qty)).filter(
            ProductMovement.product_id == product_id,
            ProductMovement.to_location == self.location_id
        ).scalar() or 0
        
        # Total sent from this location
        total_out = db.session.query(db.func.sum(ProductMovement.qty)).filter(
            ProductMovement.product_id == product_id,
            ProductMovement.from_location == self.location_id
        ).scalar() or 0
        
        return total_in - total_out
    
    def __repr__(self):
        return f'<Location {self.location_id}: {self.name}>'


class ProductMovement(db.Model):
    """ProductMovement model for tracking stock movements"""
    movement_id = db.Column(db.String(50), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    from_location = db.Column(db.String(50), db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.Column(db.String(50), db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.String(50), db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    
    # Relationships
    product = db.relationship('Product', backref=db.backref('movements', lazy=True))
    from_loc = db.relationship('Location', foreign_keys=[from_location], backref=db.backref('movements_from', lazy=True))
    to_loc = db.relationship('Location', foreign_keys=[to_location], backref=db.backref('movements_to', lazy=True))
    
    def get_movement_type(self):
        """Determine movement type: Inbound, Outbound, or Transfer"""
        if self.from_location is None and self.to_location is not None:
            return "Inbound"
        elif self.from_location is not None and self.to_location is None:
            return "Outbound"
        elif self.from_location is not None and self.to_location is not None:
            return "Transfer"
        else:
            return "Unknown"
    
    def validate_movement(self):
        """Validate if movement is possible (check stock availability)"""
        if self.from_location:
            # Check if there's enough stock at source location
            location = Location.query.get(self.from_location)
            if location:
                available_qty = location.get_product_qty(self.product_id)
                if available_qty < self.qty:
                    return False, f"Insufficient stock at {location.name}. Available: {available_qty}, Required: {self.qty}"
        return True, "Valid movement"
    
    def __repr__(self):
        return f'<Movement {self.movement_id}: {self.product_id} from {self.from_location} to {self.to_location}>'
