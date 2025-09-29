# Restaurant Management System - Frontend

This is the Vue.js frontend for the Restaurant Management System.

## Features

- Modern Vue.js 3 application with Composition API
- Responsive design with Tailwind CSS
- Admin authentication and session management
- Menu management with image upload
- Order management with real-time status updates
- Form validation and error handling
- Toast notifications and confirmation dialogs

## Tech Stack

- **Vue.js 3**: Progressive JavaScript framework
- **Vite**: Next generation frontend tooling
- **Vue Router**: Official router for Vue.js
- **Axios**: HTTP client for API calls
- **Tailwind CSS**: Utility-first CSS framework
- **Heroicons**: Beautiful hand-crafted SVG icons

## Project Structure

```
src/
├── components/          # Reusable components
│   ├── AlertDialog.vue  # Success/error notifications
│   ├── ConfirmDialog.vue # Confirmation prompts
│   └── Navbar.vue       # Navigation component
├── views/               # Page components
│   ├── DashboardView.vue    # Admin dashboard
│   ├── LoginView.vue        # Authentication
│   ├── MenusView.vue        # Menu listing
│   ├── MenuFormView.vue     # Add/edit menu
│   ├── OrdersView.vue       # Order listing
│   └── OrderFormView.vue    # Add/edit order
├── services/            # API service layer
│   ├── api.js          # Axios configuration
│   ├── auth.js         # Authentication service
│   ├── menu.js         # Menu API calls
│   └── order.js        # Order API calls
├── App.vue             # Root component
├── main.js             # Application entry point
├── router.js           # Route configuration
└── style.css           # Global styles
```

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## Features

### Authentication
- Secure login system with session management
- Route guards to protect admin areas
- Automatic redirect on authentication failure

### Dashboard
- Key statistics (total menus, orders, revenue)
- Recent orders overview
- Quick action buttons
- Responsive design for all screen sizes

### Menu Management
- Create, read, update, delete menu items
- Image upload with preview
- Category-based organization
- Search and filter functionality
- Pagination for large datasets
- Form validation

### Order Management
- Create orders with multiple menu items
- Real-time status updates (pending/completed/cancelled)
- Customer information management
- Order notes and special instructions
- Comprehensive order history

### User Experience
- Responsive mobile-first design
- Loading states and error handling
- Success/error toast notifications
- Confirmation dialogs for destructive actions
- Intuitive navigation and breadcrumbs

## API Integration

The frontend communicates with the Flask backend through a service layer:

### Authentication Service
```javascript
// Login
await authService.login(username, password)

// Check authentication status
const isAuthenticated = await authService.checkAuth()

// Logout
await authService.logout()
```

### Menu Service
```javascript
// Get menus with pagination/search
const data = await menuService.getMenus({ 
  page: 1, 
  per_page: 10, 
  search: 'query',
  category: 'Main Course' 
})

// Create menu
await menuService.createMenu(menuData)

// Upload image
const response = await menuService.uploadImage(file)
```

### Order Service
```javascript
// Get orders
const data = await orderService.getOrders({ status: 'pending' })

// Create order
await orderService.createOrder({
  customer_name: 'John Doe',
  items: [{ menu_id: 1, quantity: 2 }]
})

// Update status
await orderService.updateOrderStatus(orderId, 'completed')
```

## Styling

The application uses Tailwind CSS with a custom color scheme:

```javascript
// Primary color palette
primary: {
  50: '#fef7ee',
  100: '#fdedd3',
  200: '#fbd7a5',
  300: '#f8bc6d',
  400: '#f59833',
  500: '#f37f0c',  // Main brand color
  600: '#e46407',
  700: '#bd4b08',
  800: '#983c0e',
  900: '#7c320f',
  950: '#431605',
}
```

## Form Validation

Comprehensive validation on both client and server side:

- Required field validation
- Data type validation (numbers, emails)
- Business rule validation (price > 0, quantity > 0)
- File type and size validation for uploads
- Real-time validation feedback

## Error Handling

Robust error handling throughout the application:

- Network error recovery
- API error display
- Graceful degradation
- User-friendly error messages
- Retry mechanisms where appropriate

## Development

### Code Style
- Vue.js 3 Options API for consistency
- ES6+ JavaScript features
- Semantic HTML structure
- Accessible design patterns

### Performance
- Lazy loading for routes
- Image optimization
- Efficient API calls with pagination
- Minimal bundle size with Vite

## Deployment

Build the application for production:

```bash
npm run build
```

The built files will be in the `dist/` directory and can be served by any static file server.

For deployment with a reverse proxy (nginx example):

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    root /path/to/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```