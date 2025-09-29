# Restaurant Management System - Backend

This is the Flask-based backend API for the Restaurant Management System.

## Features

- RESTful API endpoints for menu and order management
- MySQL database with SQLAlchemy ORM
- Admin authentication with Flask-Login
- Image upload functionality
- CORS support for frontend integration
- Comprehensive error handling and validation
- PDF export functionality with ReportLab for order reports and receipts

## API Endpoints

### Authentication
- `POST /api/auth/login` - Admin login
- `POST /api/auth/logout` - Admin logout
- `GET /api/auth/status` - Check authentication status
- `GET /api/auth/me` - Get current user info

### Menu Management
- `GET /api/menus` - Get menus (supports pagination, search, category filter)
- `GET /api/menus/{id}` - Get specific menu item
- `POST /api/menus` - Create new menu item (requires auth)
- `PUT /api/menus/{id}` - Update menu item (requires auth)
- `DELETE /api/menus/{id}` - Delete menu item (requires auth)
- `GET /api/menus/categories` - Get all menu categories
- `POST /api/menus/upload-image` - Upload menu image (requires auth)

### Order Management
- `GET /api/orders` - Get orders (supports pagination, status filter) (requires auth)
- `GET /api/orders/{id}` - Get specific order (requires auth)
- `POST /api/orders` - Create new order
- `PUT /api/orders/{id}` - Update order (requires auth)
- `DELETE /api/orders/{id}` - Delete order (requires auth)
- `PUT /api/orders/{id}/status` - Update order status (requires auth)
- `GET /api/orders/export-pdf` - Export all orders to PDF (supports status filter) (requires auth)
- `GET /api/orders/{id}/export-pdf` - Export single order receipt to PDF (requires auth)

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. Create MySQL database:
   ```sql
   CREATE DATABASE restaurant_db;
   ```

5. Initialize database:
   ```bash
   flask init-db
   ```

6. Run the server:
   ```bash
   python run.py
   ```

## Database Schema

### Admin Table
- id (Primary Key)
- username (Unique)
- password_hash
- created_at

### Menu Table
- id (Primary Key)
- name
- description
- price
- category
- image_url
- is_available
- created_at
- updated_at

### Order Table
- id (Primary Key)
- customer_name
- status (enum: pending, completed, cancelled)
- total_amount
- notes
- created_at
- updated_at

### OrderItem Table
- id (Primary Key)
- order_id (Foreign Key)
- menu_id (Foreign Key)
- quantity
- price (price at time of order)

## Configuration

The application uses the following environment variables:

- `DATABASE_URL`: MySQL connection string
- `SECRET_KEY`: Flask secret key for sessions
- `FLASK_ENV`: Environment (development/production)
- `UPLOAD_FOLDER`: Directory for uploaded images
- `MAX_CONTENT_LENGTH`: Maximum file upload size

## Default Data

The `flask init-db` command creates:
- Default admin user (username: admin, password: admin123)
- Sample menu items across different categories

## Error Handling

The API returns consistent JSON error responses:

```json
{
  "error": "Error message",
  "details": "Additional details (optional)"
}
```

HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

## Dependencies

### Core Dependencies
- **Flask 2.3.3**: Web framework
- **Flask-SQLAlchemy 3.0.5**: Database ORM
- **Flask-Login 0.6.3**: Authentication management
- **Flask-CORS 4.0.0**: Cross-origin resource sharing
- **PyMySQL 1.1.0**: MySQL database connector
- **ReportLab 4.0.4**: PDF generation library
- **Werkzeug 2.3.7**: WSGI utilities and file upload handling
- **python-dotenv 1.0.0**: Environment variable management
- **cryptography 41.0.4**: Password hashing and security

### PDF Export Features
- Professional order reports with company branding
- Summary statistics (total orders, revenue, status breakdown)
- Detailed order tables with customer information and items
- Individual order receipts for customer transactions
- Automatic file naming with timestamps
- Support for status filtering in bulk exports