from app import db
from datetime import datetime
from sqlalchemy import Numeric

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum('pending', 'completed', 'cancelled', name='order_status'), default='pending')
    total_amount = db.Column(Numeric(10, 2), nullable=False, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with order items
    order_items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    
    def calculate_total(self):
        """Calculate total amount from order items"""
        total = sum(item.quantity * item.price for item in self.order_items)
        self.total_amount = total
        return total
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'status': self.status,
            'total_amount': float(self.total_amount),
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'order_items': [item.to_dict() for item in self.order_items]
        }
    
    def __repr__(self):
        return f'<Order {self.id} - {self.customer_name}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(Numeric(10, 2), nullable=False)  # Price at the time of order
    
    # Relationships
    order = db.relationship('Order', back_populates='order_items')
    menu = db.relationship('Menu', back_populates='order_items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'menu_id': self.menu_id,
            'menu_name': self.menu.name if self.menu else None,
            'quantity': self.quantity,
            'price': float(self.price),
            'subtotal': float(self.quantity * self.price)
        }
    
    def __repr__(self):
        return f'<OrderItem {self.id} - Menu {self.menu_id} x{self.quantity}>'