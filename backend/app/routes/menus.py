from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required
from app import db
from app.models.menu import Menu
import os
from werkzeug.utils import secure_filename
import uuid

bp = Blueprint('menus', __name__, url_prefix='/api/menus')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('', methods=['GET'])
def get_menus():
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        category = request.args.get('category', '')
        
        # Build query
        query = Menu.query
        
        if search:
            query = query.filter(Menu.name.contains(search))
        
        if category:
            query = query.filter(Menu.category == category)
        
        # Order by created_at desc
        query = query.order_by(Menu.created_at.desc())
        
        # Paginate
        menus = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'menus': [menu.to_dict() for menu in menus.items],
            'total': menus.total,
            'pages': menus.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch menus', 'details': str(e)}), 500

@bp.route('/<int:menu_id>', methods=['GET'])
def get_menu(menu_id):
    try:
        menu = Menu.query.get_or_404(menu_id)
        return jsonify({'menu': menu.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': 'Menu not found', 'details': str(e)}), 404

@bp.route('', methods=['POST'])
@login_required
def create_menu():
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('name') or not data.get('price') or not data.get('category'):
            return jsonify({'error': 'Name, price, and category are required'}), 400
        
        if data['price'] <= 0:
            return jsonify({'error': 'Price must be greater than 0'}), 400
        
        # Create menu
        menu = Menu(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            category=data['category'],
            image_url=data.get('image_url', ''),
            is_available=data.get('is_available', True)
        )
        
        db.session.add(menu)
        db.session.commit()
        
        return jsonify({
            'message': 'Menu created successfully',
            'menu': menu.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create menu', 'details': str(e)}), 500

@bp.route('/<int:menu_id>', methods=['PUT'])
@login_required
def update_menu(menu_id):
    try:
        menu = Menu.query.get_or_404(menu_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validation
        if 'price' in data and data['price'] <= 0:
            return jsonify({'error': 'Price must be greater than 0'}), 400
        
        # Update fields
        if 'name' in data:
            menu.name = data['name']
        if 'description' in data:
            menu.description = data['description']
        if 'price' in data:
            menu.price = data['price']
        if 'category' in data:
            menu.category = data['category']
        if 'image_url' in data:
            menu.image_url = data['image_url']
        if 'is_available' in data:
            menu.is_available = data['is_available']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Menu updated successfully',
            'menu': menu.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update menu', 'details': str(e)}), 500

@bp.route('/<int:menu_id>', methods=['DELETE'])
@login_required
def delete_menu(menu_id):
    try:
        menu = Menu.query.get_or_404(menu_id)
        
        db.session.delete(menu)
        db.session.commit()
        
        return jsonify({'message': 'Menu deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete menu', 'details': str(e)}), 500

@bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = db.session.query(Menu.category).distinct().all()
        categories = [cat[0] for cat in categories]
        return jsonify({'categories': categories}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch categories', 'details': str(e)}), 500

@bp.route('/upload-image', methods=['POST'])
@login_required
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{uuid.uuid4().hex}{ext}"
            
            # Save file
            upload_path = os.path.join(current_app.instance_path, '..', 'static', 'uploads')
            os.makedirs(upload_path, exist_ok=True)
            file_path = os.path.join(upload_path, filename)
            file.save(file_path)
            
            # Return URL
            image_url = f"/static/uploads/{filename}"
            return jsonify({
                'message': 'Image uploaded successfully',
                'image_url': image_url
            }), 200
        else:
            return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG, GIF allowed'}), 400
            
    except Exception as e:
        return jsonify({'error': 'Failed to upload image', 'details': str(e)}), 500