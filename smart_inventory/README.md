# Smart Inventory Management System

A full-stack inventory management system built with Python, Django, MySQL, and Pandas.

---

## Project Structure

```
smart_inventory/
│
├── core/                          # Part 1 — Core Business Logic (OOP)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product.py             # Product class with stock management
│   │   ├── customer.py            # Customer class with email validation
│   │   ├── order.py               # Order class with item management
│   │   └── order_item.py          # OrderItem class with subtotal
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── exceptions.py          # OutOfStockException, InvalidEmailException, InvalidQuantityException
│   └── services/
│       ├── __init__.py
│       └── inventory_service.py   # High-level business operations
│
├── database/                      # Part 2 — Database Layer (MySQL + DAO)
│   ├── dao/
│   │   ├── __init__.py
│   │   ├── base_dao.py            # Abstract DAO interface
│   │   ├── product_dao.py         # ProductDAO (CRUD)
│   │   ├── customer_dao.py        # CustomerDAO (CRUD)
│   │   └── order_dao.py           # OrderDAO with transaction management
│   ├── connection.py              # MySQL connection helper
│   ├── schema.sql                 # Database schema (CREATE TABLE)
│   └── populate.sql               # Sample data population script
│
├── web/                           # Part 3 — Django Web Application
│   ├── manage.py
│   ├── django_project/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── inventory/                 # Django app
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py              # Django ORM models
│   │   ├── forms.py               # Custom forms with validation
│   │   ├── views.py               # Views (CRUD + Dashboard)
│   │   ├── urls.py                # URL routing
│   │   └── admin.py               # Admin panel configuration
│   └── templates/                 # Enhanced HTML templates
│       ├── base.html              # Base template with sidebar & Bootstrap 5
│       └── inventory/
│           ├── dashboard.html     # KPI dashboard
│           ├── product_list.html
│           ├── product_form.html
│           ├── product_detail.html
│           ├── product_confirm_delete.html
│           ├── customer_list.html
│           ├── customer_form.html
│           ├── customer_confirm_delete.html
│           ├── order_list.html
│           ├── order_form.html
│           └── order_detail.html
│
├── analytics/                     # Part 4 — Data Analysis
│   ├── analysis.ipynb             # Jupyter notebook with full analysis
│   ├── export_data.py             # MySQL → CSV exporter
│   └── data/                      # Sample CSV files
│       ├── products.csv
│       ├── customers.csv
│       ├── orders.csv
│       └── order_items.csv
│
├── tests/
│   ├── __init__.py
│   └── test_models.py             # Unit tests for core models
│
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## Setup Instructions

### Prerequisites

- **Python** 3.10+
- **MySQL** 8.0+
- **pip** (Python package manager)

### 1. Clone & Install Dependencies

```bash
cd smart_inventory
pip install -r requirements.txt
```

### 2. Set Up the MySQL Database

```sql
-- Connect to MySQL and run:
SOURCE database/schema.sql;
SOURCE database/populate.sql;
```

Or via terminal:

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/populate.sql
```

### 3. Configure Database Credentials

Edit the following files with your MySQL credentials:

- `database/connection.py` — update `DB_CONFIG["password"]`
- `web/django_project/settings.py` — update `DATABASES["default"]["PASSWORD"]`

### 4. Run Django Migrations

```bash
cd web
python manage.py migrate
python manage.py createsuperuser   # Create an admin user
python manage.py runserver
```

Visit http://127.0.0.1:8000/ for the web interface.  
Visit http://127.0.0.1:8000/admin/ for the admin panel.

### 5. Run Unit Tests

```bash
cd smart_inventory
python -m pytest tests/ -v
# or
python tests/test_models.py
```

### 6. Run Data Analysis

```bash
cd analytics
jupyter notebook analysis.ipynb
```

Or to export fresh data from MySQL first:

```bash
python analytics/export_data.py
```

---

## Architecture & Data Flow

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│  Core Layer      │     │  Database    │     │  Web Layer       │
│  (OOP Models)    │────▶│  (MySQL +   │◀───▶│  (Django)        │
│  + Exceptions    │     │   DAO)       │     │  + Templates     │
└─────────────────┘     └──────┬───────┘     └──────────────────┘
                               │
                               ▼
                     ┌──────────────────┐
                     │  Analytics Layer │
                     │  (Pandas/NumPy)  │
                     │  + Jupyter       │
                     └──────────────────┘
```

### Exception Propagation

1. **Core Layer** raises `OutOfStockException`, `InvalidEmailException`, `InvalidQuantityException`
2. **DAO Layer** catches DB errors, rolls back transactions, re-raises
3. **Django Layer** converts exceptions to user-friendly form errors / flash messages
4. **Logging** via Python `logging` module tracks all errors to console + `debug.log`

---

## Features

### Web Interface
- **Dashboard** with KPI cards (products, customers, orders, revenue, stock value)
- **Product CRUD** — create, view, edit, delete products with stock badges
- **Customer Registration** — with email validation
- **Order Management** — create orders with inline item formset, stock deduction
- **Order History** — view all orders with details
- **Admin Panel** — full Django admin with inline order items

### Analytics
- Total revenue per month (bar chart)
- Best-selling products (horizontal bar chart)
- Stock value by category (pie chart)
- Average order value with statistics (histogram)
- Customer purchase frequency (bar chart)
- Business insights report

---

## Technologies Used

| Layer | Technology |
|-------|-----------|
| Core Business Logic | Python 3, OOP, Custom Exceptions |
| Database | MySQL 8, mysql-connector-python |
| Web Framework | Django 5.x |
| Frontend | Bootstrap 5.3, Bootstrap Icons |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Testing | unittest / pytest |

---

## License

This project is for educational purposes.
