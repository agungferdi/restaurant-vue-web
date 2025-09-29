from app import create_app, db
from app.models.admin import Admin
from app.models.menu import Menu
from app.models.order import Order, OrderItem

app = create_app()

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    
    # Create default admin user
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
    # Add sample menu items
    if Menu.query.count() == 0:
        sample_menus = [
            Menu(name='Nasi Goreng', description='Indonesian fried rice with chicken and vegetables', price=25000, category='Main Course'),
            Menu(name='Mie Ayam', description='Chicken noodle soup with vegetables', price=20000, category='Main Course'),
            Menu(name='Gado-Gado', description='Indonesian vegetable salad with peanut sauce', price=18000, category='Salad'),
            Menu(name='Sate Ayam', description='Grilled chicken skewers with peanut sauce', price=30000, category='Grilled'),
            Menu(name='Es Teh Manis', description='Sweet iced tea', price=8000, category='Beverage'),
            Menu(name='Es Jeruk', description='Fresh orange juice with ice', price=12000, category='Beverage'),
            Menu(name='Pisang Goreng', description='Fried banana with crispy coating', price=15000, category='Dessert'),
            Menu(name='Es Cendol', description='Traditional Indonesian dessert with coconut milk', price=18000, category='Dessert'),
        ]
        
        for menu in sample_menus:
            db.session.add(menu)
    
    db.session.commit()
    print('Database initialized successfully!')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)