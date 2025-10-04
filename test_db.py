#!/usr/bin/env python3
"""Test script to check database operations"""

from app import app, db, Product

def test_add_product():
    with app.app_context():
        # Try to add a test product
        test_product = Product(
            product_id="TEST123",
            name="Test Product",
            description="This is a test product"
        )
        
        try:
            db.session.add(test_product)
            db.session.commit()
            print("SUCCESS: Product added successfully!")
            
            # Verify it was added
            found_product = Product.query.get("TEST123")
            if found_product:
                print(f"SUCCESS: Product found: {found_product.name}")
            else:
                print("ERROR: Product not found after adding")
                
        except Exception as e:
            print(f"ERROR: Error adding product: {e}")
            db.session.rollback()
        
        # Clean up
        try:
            product_to_delete = Product.query.get("TEST123")
            if product_to_delete:
                db.session.delete(product_to_delete)
                db.session.commit()
                print("SUCCESS: Test product cleaned up")
        except Exception as e:
            print(f"ERROR: Error cleaning up: {e}")

if __name__ == "__main__":
    test_add_product()