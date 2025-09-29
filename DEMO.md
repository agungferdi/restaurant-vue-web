# Restaurant Management System - Demo Instructions

## Quick Demo Setup

This guide will help you quickly set up and demo the Restaurant Management System.

### Prerequisites Check
- Python 3.8+ installed
- Node.js 16+ installed  
- MySQL 8.0+ installed and running

### 1. Database Setup (2 minutes)

```bash
# Create database
mysql -u root -p
```

```sql
CREATE DATABASE restaurant_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'restaurant_user'@'localhost' IDENTIFIED BY 'restaurant_pass';
GRANT ALL PRIVILEGES ON restaurant_db.* TO 'restaurant_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 2. Backend Setup (3 minutes)

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and update DATABASE_URL:
# DATABASE_URL=mysql+pymysql://restaurant_user:restaurant_pass@localhost/restaurant_db

# Initialize database with sample data
python init_db.py

# Start backend server
python run.py
```

Backend will run at: **http://localhost:5000**

### 3. Frontend Setup (2 minutes)

```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Start frontend server
npm run dev
```

Frontend will run at: **http://localhost:3000**

### 4. Demo Login

Open **http://localhost:3000** in your browser

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

## Demo Features Walkthrough

### 1. Dashboard Overview
- View key statistics (menus, orders, revenue)
- See recent orders
- Quick action buttons

### 2. Menu Management
- **View Menus**: Browse with pagination and search
- **Add Menu**: Create new menu with image upload
- **Edit Menu**: Update existing menu items
- **Delete Menu**: Remove menu items with confirmation
- **Filter**: By category and availability
- **Search**: Real-time search functionality

### 3. Order Management
- **View Orders**: List with status filtering
- **Create Order**: Multi-item order creation
- **Update Status**: One-click status changes (pending → completed)
- **Edit Orders**: Modify order details
- **Delete Orders**: Remove orders with confirmation

### 4. Advanced Features
- **Image Upload**: Menu photos with preview
- **Form Validation**: Client and server-side validation
- **Toast Notifications**: Success/error messages
- **Confirmation Dialogs**: Prevent accidental actions
- **Responsive Design**: Works on all devices
- **Real-time Search**: Instant search results
- **Pagination**: Efficient data loading

## Sample Data Included

The system comes with:
- **15 Sample Menu Items** across 5 categories:
  - Main Course: Nasi Goreng, Rendang, Mie Ayam, etc.
  - Appetizers: Bakwan Jagung, Kerupuk Udang
  - Beverages: Es Teh, Jus Alpukat, Es Jeruk
  - Desserts: Martabak Manis, Es Cendol, Pisang Goreng
  - Salads: Gado-Gado

- **2 Sample Orders** with different statuses for testing

## API Testing

Backend API is available at `http://localhost:5000/api`

### Test Endpoints:
```bash
# Get all menus
curl http://localhost:5000/api/menus

# Login (get session)
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Create new order
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Demo Customer",
    "items": [{"menu_id": 1, "quantity": 2}]
  }'
```

## Architecture Highlights

**Backend**: Flask with SQLAlchemy ORM  
**Frontend**: Vue.js 3 with Tailwind CSS  
**Database**: MySQL with proper relationships  
**Authentication**: Session-based with Flask-Login  
**Validation**: Comprehensive form validation  
**File Upload**: Secure image handling  
**CORS**: Configured for development  
**Error Handling**: Graceful error management  
**Responsive**: Mobile-first design  

## Production Deployment Notes

For production deployment:

1. **Backend**: Use Gunicorn + Nginx
2. **Frontend**: Build with `npm run build` and serve static files
3. **Database**: Configure production MySQL with proper security
4. **Environment**: Update `.env` with production values
5. **Security**: Change default admin password and secret keys

## Troubleshooting

### Common Issues:

1. **Database Connection Error**:
   - Verify MySQL is running
   - Check credentials in `.env`
   - Ensure database exists

2. **Frontend Not Loading**:
   - Check if backend is running on port 5000
   - Verify Vite proxy configuration

3. **Image Upload Issues**:
   - Check `static/uploads` directory permissions
   - Verify MAX_CONTENT_LENGTH setting

### Reset Database:
```bash
cd backend
python init_db.py  # Reinitialize with fresh sample data
```

---

**Demo Time**: ~10 minutes total setup  
**Features**: All requirements + bonus features implemented  
**Status**: Production-ready with comprehensive documentation