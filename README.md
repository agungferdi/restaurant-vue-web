# Restaurant Management System

A full-stack web application for restaurant management built with Flask (backend) and Vue.js (frontend).

## Demo Video

**[Watch Live Demo Testing](https://drive.google.com/file/d/1W-iyn8K_qJi-DgyDxEx_Wx0yKE-9SJQw/view?usp=sharing)** - Complete walkthrough of all features 
## Features

### Menu Management
- Add new menu items (name, description, price, category, optional image)
- View menu list with pagination and search functionality
- Edit existing menu items
- Delete menu items
- Category-based filtering
- Image upload for menu items
- Availability toggle

### Order Management
- Create new orders (select menu items, quantity, customer name)
- View order list with status (pending, completed, cancelled)
- Update order status with one-click actions
- Edit order details and items
- Delete orders
- Order notes and special instructions
- Real-time order tracking
- **PDF Export**: Export all orders or filtered orders to professionally formatted PDF reports
- **Individual Order Receipts**: Generate PDF receipts for single orders

### Authentication & Dashboard
- Simple admin login system with session management
- Secure authentication with Flask-Login
- Dashboard with key statistics
- Recent orders overview
- Quick action buttons

### User Experience
- Responsive design with Tailwind CSS
- Form validation on frontend and backend
- Success/error notifications
- Confirmation dialogs for destructive actions
- Intuitive navigation

## Tech Stack

### Backend
- **Framework**: Flask 2.3.3
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **CORS**: Flask-CORS
- **File Upload**: Werkzeug
- **Migration**: Flask-Migrate
- **PDF Generation**: ReportLab for PDF reports and receipts

### Frontend
- **Framework**: Vue.js 3
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **Styling**: Tailwind CSS 3
- **Icons**: Heroicons
- **Routing**: Vue Router 4

## Project Structure

```
restaurant/
├── backend/                    # Flask API server
│   ├── app/
│   │   ├── __init__.py        # Flask app factory
│   │   ├── models/            # Database models
│   │   │   ├── admin.py       # Admin user model
│   │   │   ├── menu.py        # Menu model
│   │   │   └── order.py       # Order & OrderItem models
│   │   └── routes/            # API endpoints
│   │       ├── auth.py        # Authentication routes
│   │       ├── menus.py       # Menu CRUD operations
│   │       └── orders.py      # Order management
│   ├── static/uploads/        # Uploaded images
│   ├── config.py              # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   ├── run.py                 # Application entry point
│   └── .env                   # Environment variables
├── frontend/                   # Vue.js application
│   ├── src/
│   │   ├── components/        # Reusable Vue components
│   │   │   ├── AlertDialog.vue
│   │   │   ├── ConfirmDialog.vue
│   │   │   └── Navbar.vue
│   │   ├── views/             # Page components
│   │   │   ├── DashboardView.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── MenusView.vue
│   │   │   ├── MenuFormView.vue
│   │   │   ├── OrdersView.vue
│   │   │   └── OrderFormView.vue
│   │   ├── services/          # API service layer
│   │   │   ├── api.js         # Axios configuration
│   │   │   ├── auth.js        # Authentication service
│   │   │   ├── menu.js        # Menu service
│   │   │   └── order.js       # Order service
│   │   ├── App.vue            # Root component
│   │   ├── main.js            # Application entry point
│   │   ├── router.js          # Vue Router configuration
│   │   └── style.css          # Global styles
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   └── postcss.config.js      # PostCSS configuration
└── README.md                   # This documentation
```

## Screenshots

### Login Page
![Login Page](images/login.png)
*Secure admin authentication with session management and form validation for username/password fields.*

### Dashboard
![Dashboard](images/dashboard.png)
*Overview of key statistics including total menus, orders, revenue, and recent orders with real-time data.*

### Menu Management
![Menu Management](images/menus_page.png)
*Complete menu listing with search functionality, category filtering, and pagination for efficient browsing.*

![Add Menu Form](images/add_menus_form.png)
*Menu creation form with comprehensive validation including required fields (name, price, category), price validation (must be > 0), file type validation for images (PNG, JPG, JPEG, GIF up to 10MB), and availability toggle.*

![Menu Success Notification](images/notification_menu.png)
*Success feedback with toast notifications for all CRUD operations.*

### Order Management
![Order Management](images/orders.png)
*Order tracking system where status reflects payment state: **Pending** = customer hasn't paid bill yet (can pay after eating), **Completed** = bill paid, **Cancelled** = order cancelled. Includes search by customer name and status filtering.*

![New Order Form](images/new_order_form.png)
*Order creation with validation for customer name (required), at least one menu item, quantity validation (must be > 0), menu availability check, and automatic total calculation. Status can be set to Pending or Completed during creation.*

![Order Success Notification](images/notification_order.png)
*Confirmation notifications for order operations with automatic redirect after successful creation.*

### PDF Export Feature
![PDF Export Result](images/pdf_result.png)
*Professional PDF reports with order summary statistics and detailed order listings. Features include branded headers, formatted tables, and automatic file naming with timestamps. Supports filtering by status for targeted reports.*

## Quick Start

### Prerequisites
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **MySQL**: 8.0 or higher

### Step 1: Clone and Setup Backend

1. Navigate to backend directory:
   ```bash
   cd restaurant/backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Setup MySQL database:
   ```sql
   CREATE DATABASE restaurant_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'restaurant_user'@'localhost' IDENTIFIED BY 'secure_password';
   GRANT ALL PRIVILEGES ON restaurant_db.* TO 'restaurant_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

5. Configure environment variables (create `.env` file):
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-super-secret-key-change-this-in-production
   DATABASE_URL=mysql+pymysql://restaurant_user:secure_password@localhost/restaurant_db
   ```

6. Initialize database with sample data:
   ```bash
   flask init-db
   ```

7. Start the backend server:
   ```bash
   python run.py
   ```
   Backend will be available at: http://localhost:5000

### Step 2: Setup Frontend

1. Navigate to frontend directory:
   ```bash
   cd restaurant/frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   Frontend will be available at: http://localhost:3000

### Step 3: Access the Application

1. Open your browser and go to: **http://localhost:3000**
2. Login with default credentials:
   - **Username**: `admin`
   - **Password**: `admin123`

## API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/auth/login` | Admin login | No |
| POST | `/api/auth/logout` | Admin logout | Yes |
| GET | `/api/auth/status` | Check auth status | No |
| GET | `/api/auth/me` | Get current user | Yes |

#### Login Request:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

### Menu Management Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/menus` | Get menus with pagination/search | No |
| GET | `/api/menus/{id}` | Get specific menu | No |
| POST | `/api/menus` | Create new menu | Yes |
| PUT | `/api/menus/{id}` | Update menu | Yes |
| DELETE | `/api/menus/{id}` | Delete menu | Yes |
| GET | `/api/menus/categories` | Get all categories | No |
| POST | `/api/menus/upload-image` | Upload menu image | Yes |

#### Menu Object:
```json
{
  "id": 1,
  "name": "Nasi Goreng Special",
  "description": "Indonesian fried rice with chicken and vegetables",
  "price": 25000,
  "category": "Main Course",
  "image_url": "/static/uploads/menu-image.jpg",
  "is_available": true,
  "created_at": "2023-10-01T10:00:00",
  "updated_at": "2023-10-01T10:00:00"
}
```

### Order Management Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/orders` | Get orders with pagination/filtering | Yes |
| GET | `/api/orders/{id}` | Get specific order | Yes |
| POST | `/api/orders` | Create new order | No |
| PUT | `/api/orders/{id}` | Update order | Yes |
| DELETE | `/api/orders/{id}` | Delete order | Yes |
| PUT | `/api/orders/{id}/status` | Update order status | Yes |
| GET | `/api/orders/export-pdf` | Export all orders to PDF (supports status filter) | Yes |
| GET | `/api/orders/{id}/export-pdf` | Export single order receipt to PDF | Yes |

#### Order Object:
```json
{
  "id": 1,
  "customer_name": "John Doe",
  "status": "pending",
  "total_amount": 50000,
  "notes": "Extra spicy please",
  "created_at": "2023-10-01T10:00:00",
  "updated_at": "2023-10-01T10:00:00",
  "order_items": [
    {
      "id": 1,
      "menu_id": 1,
      "menu_name": "Nasi Goreng Special",
      "quantity": 2,
      "price": 25000,
      "subtotal": 50000
    }
  ]
}
```

## Frontend Architecture

### Component Structure
- **Views**: Page-level components for different routes
- **Components**: Reusable UI components (Navbar, Dialogs, etc.)
- **Services**: API communication layer with Axios
- **Router**: Vue Router with authentication guards

### State Management
- Component-level state using Vue 3 Composition API
- Service layer for API calls and data transformation
- Authentication state managed in auth service

### Styling Approach
- **Tailwind CSS**: Utility-first CSS framework
- **Responsive Design**: Mobile-first approach
- **Component Styling**: Scoped styles where needed
- **Design System**: Consistent color scheme and spacing

## Security Features

### Backend Security
- **Input Validation**: Comprehensive server-side validation
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **CORS Protection**: Configured for specific origins
- **File Upload Security**: Type and size validation for images
- **Session Management**: Secure session-based authentication

### Frontend Security
- **Authentication Guards**: Route-level protection
- **Input Sanitization**: Client-side validation
- **CSRF Protection**: Axios configured with credentials
- **Error Handling**: Graceful error handling without exposing sensitive data

## Testing & Validation

### Form Validation
- **Required Fields**: Client and server-side validation
- **Data Types**: Number, email, and text validation
- **Business Rules**: Price > 0, quantity > 0, etc.
- **User Feedback**: Clear error messages and success notifications

### Error Handling
- **API Errors**: Comprehensive error responses
- **Network Issues**: Connection timeout and retry logic
- **User Notifications**: Toast notifications for all actions
- **Graceful Degradation**: Fallbacks for missing data

## Production Deployment

### Backend Deployment
```bash
# Install production dependencies
pip install gunicorn

# Set production environment
export FLASK_ENV=production
export DATABASE_URL=mysql+pymysql://user:pass@host/db

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Serve with any static file server
# Files will be in dist/ directory
```

### Environment Variables
```env
# Production Backend .env
SECRET_KEY=your-super-secure-production-key
DATABASE_URL=mysql+pymysql://user:pass@production-host/restaurant_db
FLASK_ENV=production
```

## Bonus Features Implemented

1. **Image Upload**: Menu items can have images with preview
2. **Advanced Search**: Search menus by name with real-time results
3. **Category Filtering**: Filter menus by category
4. **Pagination**: Efficient data loading with pagination
5. **Status Management**: One-click order status updates
6. **Responsive Design**: Works perfectly on mobile devices
7. **Form Validation**: Comprehensive client and server validation
8. **Toast Notifications**: User-friendly success/error messages
9. **Confirmation Dialogs**: Prevent accidental deletions
10. **Dashboard Statistics**: Key metrics and recent activity

## Future Enhancements

- [ ] Customer-facing ordering interface
- [ ] Real-time notifications with WebSocket
- [ ] Payment integration
- [ ] Inventory management
- [ ] Sales reporting and analytics
- [ ] Multi-restaurant support
- [ ] Email notifications
- [ ] Print receipts functionality

## License

**Developer**: Muhammad Agung Ferdiansyah
