from flask import Blueprint, request, jsonify
from flask_login import login_required
from app import db
from app.models.order import Order, OrderItem
from app.models.menu import Menu

bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@bp.route('', methods=['GET'])
@login_required
def get_orders():
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', '')
        
        # Build query
        query = Order.query
        
        if status:
            query = query.filter(Order.status == status)
        
        # Order by created_at desc
        query = query.order_by(Order.created_at.desc())
        
        # Paginate
        orders = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'orders': [order.to_dict() for order in orders.items],
            'total': orders.total,
            'pages': orders.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch orders', 'details': str(e)}), 500

@bp.route('/<int:order_id>', methods=['GET'])
@login_required
def get_order(order_id):
    try:
        order = Order.query.get_or_404(order_id)
        return jsonify({'order': order.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': 'Order not found', 'details': str(e)}), 404

@bp.route('', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('customer_name') or not data.get('items'):
            return jsonify({'error': 'Customer name and items are required'}), 400
        
        if not isinstance(data['items'], list) or len(data['items']) == 0:
            return jsonify({'error': 'At least one item is required'}), 400
        
        # Create order
        order = Order(
            customer_name=data['customer_name'],
            notes=data.get('notes', ''),
            status='pending'
        )
        
        db.session.add(order)
        db.session.flush()  # To get the order ID
        
        # Add order items
        total_amount = 0
        for item_data in data['items']:
            if not item_data.get('menu_id') or not item_data.get('quantity'):
                return jsonify({'error': 'Menu ID and quantity are required for each item'}), 400
            
            menu = Menu.query.get(item_data['menu_id'])
            if not menu:
                return jsonify({'error': f'Menu with ID {item_data["menu_id"]} not found'}), 400
            
            if not menu.is_available:
                return jsonify({'error': f'Menu "{menu.name}" is not available'}), 400
            
            quantity = int(item_data['quantity'])
            if quantity <= 0:
                return jsonify({'error': 'Quantity must be greater than 0'}), 400
            
            order_item = OrderItem(
                order_id=order.id,
                menu_id=menu.id,
                quantity=quantity,
                price=menu.price
            )
            
            db.session.add(order_item)
            total_amount += quantity * menu.price
        
        # Update order total
        order.total_amount = total_amount
        db.session.commit()
        
        # Refresh to get order items
        db.session.refresh(order)
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': 'Invalid data format', 'details': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create order', 'details': str(e)}), 500

@bp.route('/<int:order_id>', methods=['PUT'])
@login_required
def update_order(order_id):
    try:
        order = Order.query.get_or_404(order_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields
        if 'customer_name' in data:
            order.customer_name = data['customer_name']
        
        if 'status' in data:
            if data['status'] not in ['pending', 'completed', 'cancelled']:
                return jsonify({'error': 'Invalid status. Must be pending, completed, or cancelled'}), 400
            order.status = data['status']
        
        if 'notes' in data:
            order.notes = data['notes']
        
        # Update order items if provided
        if 'items' in data:
            # Remove existing order items
            for item in order.order_items:
                db.session.delete(item)
            
            # Add new order items
            total_amount = 0
            for item_data in data['items']:
                menu = Menu.query.get(item_data['menu_id'])
                if not menu:
                    return jsonify({'error': f'Menu with ID {item_data["menu_id"]} not found'}), 400
                
                quantity = int(item_data['quantity'])
                if quantity <= 0:
                    return jsonify({'error': 'Quantity must be greater than 0'}), 400
                
                order_item = OrderItem(
                    order_id=order.id,
                    menu_id=menu.id,
                    quantity=quantity,
                    price=menu.price
                )
                
                db.session.add(order_item)
                total_amount += quantity * menu.price
            
            order.total_amount = total_amount
        
        db.session.commit()
        
        # Refresh to get updated order items
        db.session.refresh(order)
        
        return jsonify({
            'message': 'Order updated successfully',
            'order': order.to_dict()
        }), 200
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': 'Invalid data format', 'details': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update order', 'details': str(e)}), 500

@bp.route('/<int:order_id>', methods=['DELETE'])
@login_required
def delete_order(order_id):
    try:
        order = Order.query.get_or_404(order_id)
        
        db.session.delete(order)
        db.session.commit()
        
        return jsonify({'message': 'Order deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete order', 'details': str(e)}), 500

@bp.route('/<int:order_id>/status', methods=['PUT'])
@login_required
def update_order_status(order_id):
    try:
        order = Order.query.get_or_404(order_id)
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        if data['status'] not in ['pending', 'completed', 'cancelled']:
            return jsonify({'error': 'Invalid status. Must be pending, completed, or cancelled'}), 400
        
        order.status = data['status']
        db.session.commit()
        
        return jsonify({
            'message': 'Order status updated successfully',
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update order status', 'details': str(e)}), 500