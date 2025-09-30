#!/usr/bin/env python3
"""
Database initialization script with sample data
"""

from app import create_app, db
from app.models.admin import Admin
from app.models.menu import Menu
from app.models.order import Order, OrderItem

def init_database():
    """Initialize database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default admin user
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            print("Created default admin user (admin/admin123)")
        
        # Add sample menu items
        if Menu.query.count() == 0:
            sample_menus = [
                Menu(
                    name='Nasi Goreng Special',
                    description='Indonesian fried rice with chicken, egg, vegetables, and special spices',
                    price=25000,
                    category='Main Course',
                    is_available=True
                ),
                Menu(
                    name='Mie Ayam Bakso',
                    description='Chicken noodle soup with meatballs and vegetables',
                    price=20000,
                    category='Main Course',
                    is_available=True
                ),
                Menu(
                    name='Gado-Gado',
                    description='Traditional Indonesian vegetable salad with peanut sauce',
                    price=18000,
                    category='Salad',
                    is_available=True
                ),
                Menu(
                    name='Sate Ayam',
                    description='Grilled chicken skewers served with peanut sauce and rice',
                    price=30000,
                    category='Grilled',
                    is_available=True
                ),
                Menu(
                    name='Rendang Daging',
                    description='Slow-cooked beef in coconut milk and spices',
                    price=35000,
                    category='Main Course',
                    is_available=True
                ),
                Menu(
                    name='Gudeg Yogya',
                    description='Traditional Yogyakarta jackfruit curry with rice',
                    price=22000,
                    category='Main Course',
                    is_available=True
                ),
                Menu(
                    name='Bakwan Jagung',
                    description='Crispy corn fritters served with sweet chili sauce',
                    price=12000,
                    category='Appetizer',
                    is_available=True
                ),
                Menu(
                    name='Kerupuk Udang',
                    description='Traditional shrimp crackers',
                    price=8000,
                    category='Appetizer',
                    is_available=True
                ),
                Menu(
                    name='Es Teh Manis',
                    description='Sweet iced tea, refreshing traditional drink',
                    price=8000,
                    category='Beverage',
                    is_available=True
                ),
                Menu(
                    name='Es Jeruk',
                    description='Fresh orange juice served with ice',
                    price=12000,
                    category='Beverage',
                    is_available=True
                ),
                Menu(
                    name='Jus Alpukat',
                    description='Creamy avocado juice with condensed milk',
                    price=15000,
                    category='Beverage',
                    is_available=True
                ),
                Menu(
                    name='Es Campur',
                    description='Mixed ice dessert with fruits, jellies, and coconut milk',
                    price=18000,
                    category='Dessert',
                    is_available=True
                ),
                Menu(
                    name='Pisang Goreng',
                    description='Golden fried bananas with crispy coating',
                    price=15000,
                    category='Dessert',
                    is_available=True
                ),
                Menu(
                    name='Es Cendol',
                    description='Traditional Indonesian dessert with coconut milk and palm sugar',
                    price=16000,
                    category='Dessert',
                    is_available=True
                ),
                Menu(
                    name='Martabak Manis',
                    description='Sweet thick pancake with chocolate and cheese',
                    price=25000,
                    category='Dessert',
                    is_available=True
                )
            ]
            
            for menu in sample_menus:
                db.session.add(menu)
            
            print(f"✅ Created {len(sample_menus)} sample menu items")
        
        # Add sample orders
        if Order.query.count() == 0:
            # Get some menu items for sample orders
            nasi_goreng = Menu.query.filter_by(name='Nasi Goreng Special').first()
            es_teh = Menu.query.filter_by(name='Es Teh Manis').first()
            sate_ayam = Menu.query.filter_by(name='Sate Ayam').first()
            
            if nasi_goreng and es_teh and sate_ayam:
                # Sample Order 1
                order1 = Order(
                    customer_name='Budi Santoso',
                    status='pending',
                    notes='Extra pedas, tolong'
                )
                db.session.add(order1)
                db.session.flush()
                
                item1 = OrderItem(
                    order_id=order1.id,
                    menu_id=nasi_goreng.id,
                    quantity=2,
                    price=nasi_goreng.price
                )
                item2 = OrderItem(
                    order_id=order1.id,
                    menu_id=es_teh.id,
                    quantity=2,
                    price=es_teh.price
                )
                db.session.add(item1)
                db.session.add(item2)
                order1.calculate_total()
                
                # Sample Order 2
                order2 = Order(
                    customer_name='Siti Nurhaliza',
                    status='completed',
                    notes='Untuk dibawa pulang'
                )
                db.session.add(order2)
                db.session.flush()
                
                item3 = OrderItem(
                    order_id=order2.id,
                    menu_id=sate_ayam.id,
                    quantity=1,
                    price=sate_ayam.price
                )
                item4 = OrderItem(
                    order_id=order2.id,
                    menu_id=es_teh.id,
                    quantity=1,
                    price=es_teh.price
                )
                db.session.add(item3)
                db.session.add(item4)
                order2.calculate_total()
                
                print("✅ Created sample orders")
        
        # Commit all changes
        db.session.commit()
        print("Database initialization completed successfully!")

if __name__ == '__main__':
    init_database()