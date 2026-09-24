# BiteNest - Online Food Ordering Platform

BiteNest is a simple, responsive, full-stack food ordering web application built using **Python, Django, SQL, HTML5, and CSS3**.

It allows customers to explore local restaurants, view menus, manage shopping carts, place demo Cash on Delivery orders, and track order statuses. It also includes an admin dashboard for managing restaurants, food items, and customer orders.

---

## Features

### Customer Features
- **Account Management**: Register, sign in, profile view, and logout with secure password hashing.
- **Browse Restaurants**: Search and explore restaurants by name, cuisine, or keyword.
- **Restaurant Menus**: View dishes with prices, descriptions, and dietary badges (`🌱 VEG` / `🍗 NON-VEG`).
- **Cart Management**: Add items to cart, adjust quantities (+/-), and remove items.
- **Checkout & Orders**: Place demo Cash on Delivery orders and track order history (`Pending`, `Preparing`, `Out for Delivery`, `Delivered`).

### Admin Features
- **Dashboard**: View platform statistics (total restaurants, menu items, registered customers, orders).
- **Restaurant Management**: Add, edit, and delete restaurants.
- **Menu Management**: Add, edit, and delete menu items per restaurant.
- **Order Management**: View customer orders and update delivery status.

---

## Tech Stack

- **Backend**: Python, Django 5.x
- **Database**: SQLite (Local Dev) / PostgreSQL support via `DATABASE_URL` (Production)
- **Frontend**: HTML5, Custom CSS3
- **Templates**: Django Template Language (DTL)
- **Deployment**: Vercel / Render, Gunicorn, WhiteNoise, `python-dotenv`

---

## Project Structure

```
BiteNest/
│
├── manage.py                   # Django management utility
├── seed.py                     # Script to populate sample data
├── requirements.txt            # Python dependencies
├── vercel.json                 # Vercel serverless configuration
├── Procfile                    # Render / Heroku deployment command
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore settings
├── README.md                   # Project documentation
│
├── api/                        # Vercel serverless entry point
│   └── wsgi.py
│
├── meal_buddy/                 # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── delivery/                   # Main app
    ├── models.py               # Customer, Restaurant, Item, Cart, Order models
    ├── views.py                # App view handlers
    ├── urls.py                 # Route definitions
    ├── admin.py                # Admin panel setup
    ├── static/css/style.css    # Custom BiteNest CSS styles
    └── templates/delivery/     # HTML templates
        ├── base.html
        ├── index.html
        ├── about.html
        ├── signin.html
        ├── signup.html
        ├── restaurants.html
        ├── menu.html
        ├── cart.html
        ├── checkout.html
        ├── order_confirmation.html
        ├── orders.html
        ├── profile.html
        ├── admin_dashboard.html
        ├── admin_restaurants.html
        ├── add_restaurant.html
        ├── update_restaurant.html
        ├── admin_menu.html
        ├── add_menu_item.html
        ├── edit_menu_item.html
        └── admin_orders.html
```

---

## Database Schema Overview

- **Customer**: `id`, `username`, `password` (hashed), `email`, `mobile`, `address`, `role`, `created_at`
- **Restaurant**: `id`, `name`, `description`, `cuisine`, `rating`, `picture`, `created_at`
- **Item**: `id`, `restaurant_id`, `name`, `description`, `price`, `category`, `vegeterian`, `picture`
- **Cart**: `id`, `customer_id`
- **CartItem**: `id`, `item_id`, `quantity`
- **Order**: `id`, `customer_id`, `total_amount`, `status`, `delivery_address`, `contact_phone`, `created_at`
- **OrderItem**: `id`, `order_id`, `item_id`, `item_name`, `quantity`, `price`

---

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kulsumummi/BiteNest.git
   cd BiteNest
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows:
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   cp .env.example .env
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Seed sample data**
   ```bash
   python seed.py
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```
   Open `http://127.0.0.1:8000/` in your browser.

---

## Demo Credentials

- **Admin Account**: Username: `admin` | Password: `admin123`
- **Customer Account**: Username: `john_doe` | Password: `user123`

---

## Deployment Options

### Option A: Deploying on Vercel

1. **Push your code to GitHub**.
2. Go to [Vercel Dashboard](https://vercel.com/dashboard) and click **Add New Project**.
3. Import your **BiteNest** GitHub repository.
4. Set Environment Variables in Vercel:
   - `DJANGO_DEBUG` = `False`
   - `DJANGO_SECRET_KEY` = `<your-production-secret-key>`
   - `DATABASE_URL` = `<your-postgresql-url>` *(e.g. from Supabase, Neon, or ElephantSQL for persistent database storage)*
5. Click **Deploy**. Vercel will automatically detect `vercel.json` and build the application.

---

### Option B: Deploying on Render

1. Push code to GitHub.
2. Create a new **Web Service** on Render.
3. Build Command: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python seed.py`
4. Start Command: `gunicorn meal_buddy.wsgi:application`
5. Set Environment Variables:
   - `DJANGO_DEBUG` = `False`
   - `DJANGO_SECRET_KEY` = `<your-production-secret-key>`
   - `DJANGO_ALLOWED_HOSTS` = `.onrender.com`
   - `DATABASE_URL` = `<your-postgresql-url>`

---

## Future Improvements

- Digital online payment integration (Stripe / Razorpay)
- Customer ratings and reviews for restaurants
- Live map tracking for delivery drivers

---

## Author

**Ummi Kulsum**
