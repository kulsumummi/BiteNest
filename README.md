# 🍔 BiteNest – Online Food Ordering Platform

[![Live Demo](https://img.shields.io/badge/Live%20Demo-https%3A%2F%2Fbitenest--jgjn.onrender.com%2F-8e1616?style=for-the-badge&logo=render)](https://bitenest-jgjn.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Frontend](https://img.shields.io/badge/Frontend-HTML5%20%2F%20CSS3-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/)

---

## 📌 Executive Summary

**BiteNest** is a full-stack online food ordering web application designed for performance, clarity, and ease of use. Built with **Python, Django, SQL, HTML5, and CSS3**, BiteNest connects customers with local dining spots through real-time search, category filtering, interactive shopping carts, and a Cash on Delivery demo ordering system with status tracking.

The application features a dedicated administrative portal for managing restaurant listings, food menus, and delivery updates, with clean database relationships ensuring historical order accuracy.

🌐 **Live Website**: [https://bitenest-jgjn.onrender.com/](https://bitenest-jgjn.onrender.com/)

---

## 🔑 Demo Access Credentials

| Role | Username | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Customer** | `john_doe` | `user123` | Browse menus, manage cart, place COD orders, track delivery status |
| **Admin** | `admin` | `admin123` | Access admin dashboard, manage restaurants, edit menus, update order statuses |

---

## ✨ Key Features & Technical Highlights

### 🛒 Customer Experience
- **Authentication & Security**: User registration and sign-in powered by Django's PBKDF2/SHA256 password hashers and session management.
- **Restaurant Discovery**: Real-time search by restaurant name, cuisine type, or description with rating highlights.
- **Interactive Menus**: Detailed food listings featuring descriptions, prices, category filters, and dietary indicators (`🌱 VEG` / `🍗 NON-VEG`).
- **Shopping Cart**: Dynamic quantity increment/decrement, item removal, and real-time subtotal calculations.
- **Cash on Delivery Checkout**: Streamlined demo ordering flow with custom delivery address confirmation.
- **Order Tracking**: Real-time delivery status tracking (`Pending`, `Preparing`, `Out for Delivery`, `Delivered`).

### 🛠️ Administrative Control Panel
- **Analytics Dashboard**: Overview of key metrics (total restaurants, menu items, registered customers, total customer orders).
- **Restaurant Management (CRUD)**: Add new restaurants, update cuisine categories and image assets, or remove listings.
- **Menu Management (CRUD)**: Add, edit, or delete dishes per restaurant with dietary tagging.
- **Order Processing**: View customer orders and update delivery statuses.

---

## 🏗️ Technical Architecture & Design Decisions

### Data Integrity & Historical Price Preservation
To prevent database corruption when menu prices change or items are deleted, BiteNest uses decoupled `OrderItem` models. When an order is placed, unit prices and item names are frozen into the `OrderItem` record, preserving historical financial records.

```
Customer ──1:N──> Cart ──1:N──> CartItem ──N:1──> Item
   │                                               │
   └──1:N──> Order ──1:N──> OrderItem ─────────────┘ (SET_NULL on delete)
```

### Security Best Practices
- **Password Hashing**: Plaintext passwords are never stored; passwords use salted PBKDF2 algorithm.
- **Session Protection**: Route access rules ensure non-admin users cannot access administrative dashboards.
- **CSRF Token Validation**: All POST forms enforce Cross-Site Request Forgery protection.
- **Production Isolation**: Sensitive keys are loaded dynamically via environment variables (`python-dotenv`).

---

## 📁 Repository Structure

```
BiteNest/
│
├── manage.py                   # Django command utility
├── seed.py                     # Non-destructive database seeding script
├── requirements.txt            # Python package dependencies
├── Procfile                    # Render / Heroku WSGI deployment command
├── vercel.json                 # Vercel serverless configuration
├── .env.example                # Template for environment configuration
├── README.md                   # Technical documentation
│
├── api/                        # Serverless entry point
│   └── wsgi.py
│
├── meal_buddy/                 # Django core settings & routing
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── delivery/                   # Application logic
    ├── models.py               # Database schemas (Customer, Restaurant, Item, Cart, Order)
    ├── views.py                # View handlers (Auth, Restaurants, Cart, Checkout, Admin)
    ├── urls.py                 # Application route definitions
    ├── admin.py                # Django admin site registrations
    ├── static/css/style.css    # Custom BiteNest responsive design system
    └── templates/delivery/     # HTML templates using Django Template Language
```

---

## ⚙️ Local Installation & Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kulsumummi/BiteNest.git
   cd BiteNest
   ```

2. **Create & Activate Virtual Environment**
   ```bash
   # Windows:
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   ```bash
   cp .env.example .env
   ```

5. **Run Migrations & Seed Sample Data**
   ```bash
   python manage.py migrate
   python seed.py
   ```

6. **Start Development Server**
   ```bash
   python manage.py runserver
   ```
   Open `http://127.0.0.1:8000/` in your browser.

---

## 🚀 Deployment

- **Live Deployment**: Render Web Service ([https://bitenest-jgjn.onrender.com/](https://bitenest-jgjn.onrender.com/))
- **Production Server**: Gunicorn WSGI HTTP Server with WhiteNoise static asset compression.
- **Database**: PostgreSQL support via `DATABASE_URL` with SQLite fallback for local development.

---

## 👤 Author

**Ummi Kulsum**  
*Full-Stack Python & Django Developer*  
- **GitHub**: [@kulsumummi](https://github.com/kulsumummi)
- **Project Repository**: [https://github.com/kulsumummi/BiteNest](https://github.com/kulsumummi/BiteNest)
