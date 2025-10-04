# Inventory Management System

A comprehensive web-based inventory management system built with Flask that allows you to track products, locations, and movements across your organization.

## Features

- **Product Management**: Add, edit, and delete products with unique identifiers
- **Location Management**: Manage multiple warehouse/store locations
- **Movement Tracking**: Track inbound, outbound, and transfer movements
- **Balance Reports**: View current stock levels across all locations
- **User Authentication**: Secure login system with user management
- **Responsive Design**: Modern, mobile-friendly interface using Bootstrap

## Screenshots

### Dashboard
The main dashboard provides an overview of your inventory system with quick statistics and recent movements.

### Product Management
- Add new products with unique IDs
- Edit product details and descriptions
- View all products in a searchable table

### Location Management
- Create and manage multiple locations
- Track inventory across warehouses, stores, and offices

### Movement Tracking
- Record inbound movements (external → location)
- Record outbound movements (location → external)
- Record transfers between locations
- Automatic stock level updates

### Balance Reports
- View current stock levels for each product at each location
- Export capabilities for reporting

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd inventory-management-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your web browser and navigate to `http://127.0.0.1:5000`

## Default Login Credentials

- **Username**: `admin`
- **Password**: `admin123`

## Usage Guide

### Getting Started

1. **Login**: Use the default credentials or register a new account
2. **Add Locations**: Create your warehouse/store locations first
3. **Add Products**: Add products to your inventory
4. **Record Movements**: Track stock movements between locations

### Adding Products

1. Navigate to **Products** → **Add Product**
2. Fill in the required fields:
   - Product ID (unique identifier)
   - Product Name
   - Description (optional)
3. Click **Add Product**

### Adding Locations

1. Navigate to **Locations** → **Add Location**
2. Fill in the required fields:
   - Location ID (unique identifier)
   - Location Name
   - Address (optional)
3. Click **Add Location**

### Recording Movements

1. Navigate to **Movements** → **Add Movement**
2. Fill in the required fields:
   - Movement ID (unique identifier)
   - Product (select from existing products)
   - Quantity
   - From Location (leave blank for external source)
   - To Location (leave blank for external destination)
3. Click **Add Movement**

### Movement Types

- **Inbound**: External source → Location (leave "From Location" blank)
- **Outbound**: Location → External destination (leave "To Location" blank)
- **Transfer**: Location → Location (specify both locations)

## Project Structure

```
inventory-management-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── instance/
│   └── inventory.db      # SQLite database
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── script.js     # JavaScript functionality
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Dashboard
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── products.html     # Products listing
    ├── add_product.html  # Add product form
    ├── edit_product.html # Edit product form
    ├── locations.html    # Locations listing
    ├── add_location.html # Add location form
    ├── edit_location.html # Edit location form
    ├── movements.html    # Movements listing
    ├── add_movement.html # Add movement form
    ├── edit_movement.html # Edit movement form
    └── balance.html      # Balance report
```

## Database Schema

### Tables

- **user**: User authentication and profiles
- **product**: Product information and total quantities
- **location**: Location information
- **product_movement**: Movement records with timestamps

### Key Features

- Automatic stock level calculation based on movements
- Movement validation (prevents overselling)
- Audit trail with timestamps for all movements

## API Endpoints

### Authentication
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /logout` - User logout

### Products
- `GET /products` - List all products
- `GET/POST /products/add` - Add new product
- `GET/POST /products/edit/<id>` - Edit product
- `GET /products/delete/<id>` - Delete product

### Locations
- `GET /locations` - List all locations
- `GET/POST /locations/add` - Add new location
- `GET/POST /locations/edit/<id>` - Edit location
- `GET /locations/delete/<id>` - Delete location

### Movements
- `GET /movements` - List all movements
- `GET/POST /movements/add` - Add new movement
- `GET/POST /movements/edit/<id>` - Edit movement
- `GET /movements/delete/<id>` - Delete movement

### Reports
- `GET /balance` - Balance report

## Configuration

### Environment Variables

The application uses the following configuration (in `app.py`):

```python
SECRET_KEY = 'dev-secret-key-for-testing-12345'
SQLALCHEMY_DATABASE_URI = 'sqlite:///inventory.db'
WTF_CSRF_ENABLED = False  # Disabled for development
```

### Production Deployment

For production deployment:

1. **Set a secure SECRET_KEY**
2. **Enable CSRF protection**: Set `WTF_CSRF_ENABLED = True`
3. **Use a production database**: PostgreSQL or MySQL
4. **Configure proper session security**
5. **Set up HTTPS**

## Dependencies

- **Flask 2.3.3**: Web framework
- **Flask-SQLAlchemy 3.0.5**: Database ORM
- **Flask-Login 0.6.3**: User authentication
- **Flask-WTF 1.1.1**: Form handling
- **WTForms 3.0.1**: Form validation
- **Werkzeug 2.3.7**: WSGI utilities
- **email-validator**: Email validation

## Troubleshooting

### Common Issues

1. **Forms not submitting**
   - Ensure you are logged in
   - Check browser console for JavaScript errors
   - Verify all required fields are filled

2. **Database errors**
   - Delete `instance/inventory.db` to reset the database
   - Restart the application to reinitialize sample data

3. **Authentication issues**
   - Use the default credentials: admin/admin123
   - Clear browser cookies and try again
   - Check the `/debug-auth` route for authentication status

### Debug Routes

The application includes several debug routes for troubleshooting:

- `/debug-auth` - Check authentication status
- `/debug-form` - Test form submissions
- `/test-login` - Test login functionality
- `/test-session` - Check session information

## Development

### Running in Development Mode

```bash
python app.py
```

The application runs in debug mode by default with auto-reload enabled.

### Sample Data

The application automatically creates sample data on first run:

- **Users**: admin user with default credentials
- **Products**: Laptop, Mouse, Keyboard, Monitor
- **Locations**: Warehouse A, Warehouse B, Store Front, Office
- **Movements**: Sample inventory movements and transfers

### Database Reset

To reset the database and start fresh:

1. Delete the `instance/inventory.db` file
2. Restart the application
3. Sample data will be recreated automatically

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:

1. Check the troubleshooting section above
2. Review the debug routes for error information
3. Check the browser console for JavaScript errors
4. Verify all dependencies are installed correctly

## Future Enhancements

- [ ] Barcode scanning support
- [ ] Advanced reporting and analytics
- [ ] Multi-warehouse management
- [ ] Inventory alerts and notifications
- [ ] Export to Excel/CSV
- [ ] REST API for mobile apps
- [ ] Role-based access control
- [ ] Inventory forecasting

---

**Note**: This is a development version. For production use, please implement proper security measures, use a production database, and configure HTTPS.


Sample Screenshots:
image.png
image.png

image.png
image.png
image.png
image.png
image.png