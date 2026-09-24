import os
import django
import sys

# Force UTF-8 encoding for stdout on Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_buddy.settings')
django.setup()

from delivery.models import Customer, Restaurant, Item, Order, OrderItem, Cart, CartItem

def run_seed():
    force = '--force' in sys.argv

    if Restaurant.objects.exists() and not force:
        print("[!] Database already contains restaurant data. Skipping seed to prevent data loss. (Use --force to overwrite).")
        return

    print("[+] Seeding BiteNest database with initial sample data...")

    # Clear existing data cleanly if forced or fresh
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    CartItem.objects.all().delete()
    Cart.objects.all().delete()
    Item.objects.all().delete()
    Restaurant.objects.all().delete()
    Customer.objects.all().delete()

    print("[+] Cleared existing database records.")

    # 1. Create Default Admin and Customer User Accounts
    admin_user = Customer(
        username='admin',
        email='admin@bitenest.com',
        mobile='9999999999',
        address='BiteNest HQ, Tech Park, City Center',
        role='admin'
    )
    admin_user.set_password('admin123')
    admin_user.save()

    demo_customer = Customer(
        username='john_doe',
        email='john@example.com',
        mobile='9876543210',
        address='Flat 402, Sunshine Apartments, Green Avenue',
        role='customer'
    )
    demo_customer.set_password('user123')
    demo_customer.save()

    print(f"[+] Created accounts: Admin ('admin' / 'admin123') and Customer ('john_doe' / 'user123').")

    # 2. Restaurants and Menu Items Data
    restaurants_data = [
        {
            'name': 'Spice Garden',
            'cuisine': 'North Indian & Mughlai',
            'rating': 4.8,
            'description': 'Authentic rich Indian curries, aromatic biryanis, and clay-oven tandoori breads.',
            'picture': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=700&auto=format&fit=crop&q=80',
            'items': [
                {
                    'name': 'Paneer Butter Masala',
                    'description': 'Cottage cheese cubes simmered in rich, buttery tomato cream gravy with aromatic spices.',
                    'price': 280.0,
                    'category': 'Main Course',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=600&auto=format&fit=crop&q=80',
                },
                {
                    'name': 'Chicken Tikka Biryani',
                    'description': 'Aromatic basmati rice layered with juicy charcoal-grilled chicken tikka and saffron.',
                    'price': 340.0,
                    'category': 'Biryani',
                    'vegeterian': False,
                    'picture': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&auto=format&fit=crop&q=80',
                },
                {
                    'name': 'Garlic Butter Naan',
                    'description': 'Leavened flatbread freshly baked in tandoor topped with melted garlic butter.',
                    'price': 60.0,
                    'category': 'Breads',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=600&auto=format&fit=crop&q=80',
                },
                {
                    'name': 'Dal Makhani',
                    'description': 'Slow-cooked black lentils simmered overnight with cream, butter, and gentle spices.',
                    'price': 240.0,
                    'category': 'Main Course',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=600&auto=format&fit=crop&q=80',
                }
            ]
        },
        {
            'name': 'Urban Tandoor',
            'cuisine': 'Mughlai Kebabs & Rolls',
            'rating': 4.6,
            'description': 'Famous for melt-in-mouth kebabs, juicy seekh rolls, and fragrant saffron biryanis.',
            'picture': 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=700&auto=format&fit=crop&q=80',
            'items': [
                {
                    'name': 'Mutton Galouti Kebab',
                    'description': 'Finely minced spiced lamb kebabs served with mint chutney and layered paratha.',
                    'price': 390.0,
                    'category': 'Starters',
                    'vegeterian': False,
                    'picture': 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=600&auto=format&fit=crop&q=80',
                },
                {
                    'name': 'Tandoori Malai Broccoli',
                    'description': 'Broccoli florets marinated in cardamom cream cheese and slow-grilled in clay oven.',
                    'price': 290.0,
                    'category': 'Starters',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600&auto=format&fit=crop&q=80',
                },
                {
                    'name': 'Kadhai Paneer',
                    'description': 'Cottage cheese cooked with bell peppers, onions, and freshly ground kadhai masala.',
                    'price': 295.0,
                    'category': 'Main Course',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600&auto=format&fit=crop&q=80',
                }
            ]
        },
        {
            'name': 'Green Bowl',
            'cuisine': 'Healthy & Salads',
            'rating': 4.7,
            'description': 'Nourishing salad bowls, fresh cold-pressed juices, and wholesome protein wraps.',
            'picture': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=700&auto=format&fit=crop&q=80',
            'items': [
                {
                    'name': 'Avocado Quinoa Salad',
                    'description': 'Fresh hass avocado, organic quinoa, cherry tomatoes, cucumbers with lemon vinaigrette.',
                    'price': 320.0,
                    'category': 'Salads',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&auto=format&fit=crop&q=80',
                },
                {
                    'name': 'Grilled Chicken Caesar Bowl',
                    'description': 'Herb-roasted chicken breast, romaine lettuce, parmesan shavings, and house caesar dressing.',
                    'price': 350.0,
                    'category': 'Salads',
                    'vegeterian': False,
                    'picture': 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=600&auto=format&fit=crop&q=80',
                },
                {
                    'name': 'Berry Power Smoothie',
                    'description': 'Blended blueberries, strawberries, Greek yogurt, chia seeds, and honey.',
                    'price': 180.0,
                    'category': 'Beverages',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=600&auto=format&fit=crop&q=80',
                }
            ]
        },
        {
            'name': 'Pasta House',
            'cuisine': 'Italian & Artisanal Pastas',
            'rating': 4.9,
            'description': 'Handmade fresh pastas, wood-fired pizzas, garlic breads, and classic Italian desserts.',
            'picture': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=700&auto=format&fit=crop&q=80',
            'items': [
                {
                    'name': 'Fettuccine Alfredo with Mushrooms',
                    'description': 'Creamy parmesan white sauce tossed with fresh fettuccine and sautéed wild mushrooms.',
                    'price': 360.0,
                    'category': 'Pasta',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1621996346565-e3d5d6281288?w=600&auto=format&fit=crop&q=80',
                },
                {
                    'name': 'Margherita Wood-Fired Pizza',
                    'description': 'Classic Neapolitan pizza crust topped with San Marzano tomato sauce, fresh mozzarella, and basil.',
                    'price': 380.0,
                    'category': 'Pizza',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=600&auto=format&fit=crop&q=80',
                },
                {
                    'name': 'Classic Tiramisu',
                    'description': 'Traditional Italian coffee-soaked ladyfingers layered with mascarpone cheese and cocoa powder.',
                    'price': 220.0,
                    'category': 'Desserts',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=600&auto=format&fit=crop&q=80',
                }
            ]
        },
        {
            'name': 'South Plate',
            'cuisine': 'Authentic South Indian',
            'rating': 4.7,
            'description': 'Crispy paper dosas, fluffy steamed idlis, spicy Chettinad curries, and Filter Coffee.',
            'picture': 'https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?w=700&auto=format&fit=crop&q=80',
            'items': [
                {
                    'name': 'Special Masala Dosa',
                    'description': 'Golden crispy fermented rice crepe stuffed with spiced potato mash, served with coconut chutney & sambar.',
                    'price': 160.0,
                    'category': 'Dosas',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=600&auto=format&fit=crop&q=80',
                },
                {
                    'name': 'Meda Vada & Idli Combo',
                    'description': '2 soft steamed rice idlis and 1 crispy lentil medu vada served with piping hot sambar.',
                    'price': 130.0,
                    'category': 'Breakfast',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=600&auto=format&fit=crop&q=80',
                },
                {
                    'name': 'Filter Coffee',
                    'description': 'Traditional South Indian chicory decoction frothed with hot boiled milk in brass tumbler.',
                    'price': 65.0,
                    'category': 'Beverages',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&auto=format&fit=crop&q=80',
                }
            ]
        },
        {
            'name': 'Burger Junction',
            'cuisine': 'American Burgers & Fries',
            'rating': 4.5,
            'description': 'Gourmet smashed beef & crispy chicken burgers, loaded fries, and thick milkshakes.',
            'picture': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=700&auto=format&fit=crop&q=80',
            'items': [
                {
                    'name': 'Classic Double Cheese Burger',
                    'description': 'Two smashed chicken patties, double cheddar cheese, caramelized onions, pickles & secret sauce.',
                    'price': 299.0,
                    'category': 'Burgers',
                    'vegeterian': False,
                    'picture': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&auto=format&fit=crop&q=80',
                },
                {
                    'name': 'Veggie Crunch Burger',
                    'description': 'Crispy potato-veggie patty topped with lettuce, sliced tomato, jalapenos and spicy mayo.',
                    'price': 199.0,
                    'category': 'Burgers',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=600&auto=format&fit=crop&q=80',
                },
                {
                    'name': 'Peri Peri Loaded Fries',
                    'description': 'Crispy french fries tossed in spicy peri peri seasoning and drizzled with warm melted cheese.',
                    'price': 160.0,
                    'category': 'Sides',
                    'vegeterian': True,
                    'picture': 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600&auto=format&fit=crop&q=80',
                }
            ]
        }
    ]

    for rest_info in restaurants_data:
        items_data = rest_info.pop('items')
        restaurant = Restaurant.objects.create(**rest_info)
        print(f"[+] Added Restaurant: '{restaurant.name}' ({restaurant.cuisine})")
        
        for item_info in items_data:
            Item.objects.create(restaurant=restaurant, **item_info)

    # 3. Create a Sample Demo Order
    sample_order = Order.objects.create(
        customer=demo_customer,
        total_amount=680.0,
        status='Preparing',
        delivery_address=demo_customer.address,
        contact_phone=demo_customer.mobile,
    )

    item1 = Item.objects.filter(name='Paneer Butter Masala').first()
    item2 = Item.objects.filter(name='Garlic Butter Naan').first()

    if item1:
        OrderItem.objects.create(order=sample_order, item=item1, item_name=item1.name, quantity=2, price=item1.price)
    if item2:
        OrderItem.objects.create(order=sample_order, item=item2, item_name=item2.name, quantity=2, price=item2.price)

    print(f"[+] Created sample order #{sample_order.id} for customer '{demo_customer.username}'.")
    print("[SUCCESS] Database seeding complete! BiteNest is ready to run.")

if __name__ == '__main__':
    run_seed()
