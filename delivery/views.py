from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Customer, Restaurant, Item, Cart, CartItem, Order, OrderItem

def get_current_user(request):
    """Helper to get current logged in customer from session."""
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return Customer.objects.get(id=user_id)
        except Customer.DoesNotExist:
            return None
    return None

def is_admin(request):
    """Helper to check if current user has admin privileges."""
    user = get_current_user(request)
    return user is not None and (user.role == 'admin' or user.username == 'admin')

def get_common_context(request):
    """Common context variables passed to templates."""
    user = get_current_user(request)
    cart_count = 0
    if user:
        cart = Cart.objects.filter(customer=user).first()
        if cart:
            cart_count = cart.total_items()
    return {
        'current_user': user,
        'is_admin': is_admin(request),
        'cart_count': cart_count,
    }


# ==================== PUBLIC & AUTH VIEWS ====================

def index(request):
    context = get_common_context(request)
    context['featured_restaurants'] = Restaurant.objects.all()[:6]
    return render(request, 'delivery/index.html', context)

def about(request):
    context = get_common_context(request)
    return render(request, 'delivery/about.html', context)

def signup(request):
    context = get_common_context(request)
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        address = request.POST.get('address', '').strip()

        if not username or not password or not email:
            context['error'] = 'Username, email, and password are required.'
            return render(request, 'delivery/signup.html', context)

        if Customer.objects.filter(username=username).exists():
            context['error'] = f'Username "{username}" is already taken.'
            return render(request, 'delivery/signup.html', context)

        if Customer.objects.filter(email=email).exists():
            context['error'] = f'Email "{email}" is already registered.'
            return render(request, 'delivery/signup.html', context)

        customer = Customer(username=username, email=email, mobile=mobile, address=address, role='customer')
        customer.set_password(password)
        customer.save()

        request.session['user_id'] = customer.id
        request.session['username'] = customer.username
        request.session['role'] = customer.role

        messages.success(request, 'Account created successfully! Welcome to BiteNest.')
        return redirect('restaurants')

    return render(request, 'delivery/signup.html', context)

def signin(request):
    context = get_common_context(request)
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            customer = Customer.objects.get(username=username)
            if customer.check_password(password) or customer.password == password:
                if customer.password == password:
                    customer.set_password(password)
                    customer.save()

                request.session['user_id'] = customer.id
                request.session['username'] = customer.username
                request.session['role'] = customer.role

                messages.success(request, f'Welcome back, {customer.username}!')
                if customer.role == 'admin' or customer.username == 'admin':
                    return redirect('admin_dashboard')
                return redirect('restaurants')
            else:
                context['error'] = 'Invalid password. Please try again.'
        except Customer.DoesNotExist:
            context['error'] = 'Account not found. Please check your username or register.'

    return render(request, 'delivery/signin.html', context)

def logout_view(request):
    request.session.flush()
    messages.info(request, 'You have been logged out.')
    return redirect('index')

def profile(request):
    user = get_current_user(request)
    if not user:
        return redirect('signin')

    context = get_common_context(request)
    context['customer'] = user
    return render(request, 'delivery/profile.html', context)


# ==================== RESTAURANT & MENU VIEWS ====================

def restaurants(request):
    context = get_common_context(request)
    query = request.GET.get('q', '').strip()
    
    if query:
        restaurant_list = Restaurant.objects.filter(
            Q(name__icontains=query) | Q(cuisine__icontains=query) | Q(description__icontains=query)
        )
    else:
        restaurant_list = Restaurant.objects.all()

    context['restaurantList'] = restaurant_list
    context['search_query'] = query
    return render(request, 'delivery/restaurants.html', context)

def view_menu(request, restaurant_id):
    context = get_common_context(request)
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    items = restaurant.items.all()

    category = request.GET.get('category', '').strip()
    if category:
        items = items.filter(category__iexact=category)

    context['restaurant'] = restaurant
    context['itemList'] = items
    context['selected_category'] = category
    return render(request, 'delivery/menu.html', context)


# ==================== CART VIEWS ====================

def add_to_cart(request, item_id):
    user = get_current_user(request)
    if not user:
        messages.warning(request, 'Please sign in to add items to your cart.')
        return redirect('signin')

    item = get_object_or_404(Item, id=item_id)
    cart, _ = Cart.objects.get_or_create(customer=user)

    cart_item = cart.items.filter(item=item).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item = CartItem.objects.create(item=item, quantity=1)
        cart.items.add(cart_item)

    messages.success(request, f'Added "{item.name}" to your cart.')
    return redirect('view_menu', restaurant_id=item.restaurant.id)

def show_cart(request):
    user = get_current_user(request)
    if not user:
        messages.warning(request, 'Please sign in to view your cart.')
        return redirect('signin')

    context = get_common_context(request)
    cart = Cart.objects.filter(customer=user).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0.0

    context['itemList'] = items
    context['total_price'] = total_price
    return render(request, 'delivery/cart.html', context)

def increase_quantity(request, cart_item_id):
    user = get_current_user(request)
    if not user:
        return redirect('signin')

    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('show_cart')

def decrease_quantity(request, cart_item_id):
    user = get_current_user(request)
    if not user:
        return redirect('signin')

    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('show_cart')

def remove_item(request, cart_item_id):
    user = get_current_user(request)
    if not user:
        return redirect('signin')

    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    messages.info(request, 'Item removed from cart.')
    return redirect('show_cart')


# ==================== CHECKOUT & ORDERS VIEWS ====================

def checkout(request):
    user = get_current_user(request)
    if not user:
        messages.warning(request, 'Please sign in to proceed to checkout.')
        return redirect('signin')

    context = get_common_context(request)
    cart = Cart.objects.filter(customer=user).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0.0

    if not items or total_price == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('restaurants')

    context['cart_items'] = items
    context['total_price'] = total_price
    context['customer'] = user
    return render(request, 'delivery/checkout.html', context)

def place_order(request):
    user = get_current_user(request)
    if not user:
        return redirect('signin')

    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address', user.address).strip()
        contact_phone = request.POST.get('contact_phone', user.mobile).strip()

        cart = Cart.objects.filter(customer=user).first()
        if not cart or not cart.items.exists():
            messages.error(request, 'Cannot place order: Your cart is empty.')
            return redirect('restaurants')

        order = Order.objects.create(
            customer=user,
            total_amount=cart.total_price(),
            status='Pending',
            delivery_address=delivery_address or user.address,
            contact_phone=contact_phone or user.mobile,
        )

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                item_name=cart_item.item.name,
                quantity=cart_item.quantity,
                price=cart_item.item.price,
            )

        cart.items.all().delete()
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('order_confirmation', order_id=order.id)

    return redirect('checkout')

def order_confirmation(request, order_id):
    user = get_current_user(request)
    if not user:
        return redirect('signin')

    order = get_object_or_404(Order, id=order_id, customer=user)
    context = get_common_context(request)
    context['order'] = order
    context['order_items'] = order.order_items.all()
    return render(request, 'delivery/order_confirmation.html', context)

def orders(request):
    user = get_current_user(request)
    if not user:
        messages.warning(request, 'Please sign in to view your past orders.')
        return redirect('signin')

    context = get_common_context(request)
    context['orders'] = Order.objects.filter(customer=user).order_by('-created_at')
    return render(request, 'delivery/orders.html', context)


# ==================== ADMIN VIEWS ====================

def admin_dashboard(request):
    if not is_admin(request):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('signin')

    context = get_common_context(request)
    context['restaurant_count'] = Restaurant.objects.count()
    context['item_count'] = Item.objects.count()
    context['customer_count'] = Customer.objects.filter(role='customer').count()
    context['order_count'] = Order.objects.count()
    context['recent_orders'] = Order.objects.order_by('-created_at')[:5]
    return render(request, 'delivery/admin_dashboard.html', context)

def admin_restaurants(request):
    if not is_admin(request):
        messages.error(request, 'Access denied.')
        return redirect('signin')

    context = get_common_context(request)
    context['restaurantList'] = Restaurant.objects.all()
    return render(request, 'delivery/admin_restaurants.html', context)

def add_restaurant(request):
    if not is_admin(request):
        return redirect('signin')

    context = get_common_context(request)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        picture = request.POST.get('picture', '').strip()
        cuisine = request.POST.get('cuisine', '').strip()
        rating = float(request.POST.get('rating', 4.5))
        description = request.POST.get('description', '').strip()

        if Restaurant.objects.filter(name=name).exists():
            context['error'] = f'Restaurant "{name}" already exists.'
            return render(request, 'delivery/add_restaurant.html', context)

        Restaurant.objects.create(
            name=name,
            picture=picture or 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600',
            cuisine=cuisine,
            rating=rating,
            description=description or 'Delicious dishes served fresh.'
        )
        messages.success(request, f'Restaurant "{name}" added successfully.')
        return redirect('admin_restaurants')

    return render(request, 'delivery/add_restaurant.html', context)

def update_restaurant(request, restaurant_id):
    if not is_admin(request):
        return redirect('signin')

    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    context = get_common_context(request)
    context['restaurant'] = restaurant

    if request.method == 'POST':
        restaurant.name = request.POST.get('name', '').strip()
        restaurant.cuisine = request.POST.get('cuisine', '').strip()
        restaurant.rating = float(request.POST.get('rating', 4.5))
        restaurant.picture = request.POST.get('picture', '').strip()
        restaurant.description = request.POST.get('description', '').strip()
        restaurant.save()

        messages.success(request, f'Restaurant "{restaurant.name}" updated successfully.')
        return redirect('admin_restaurants')

    return render(request, 'delivery/update_restaurant.html', context)

def delete_restaurant(request, restaurant_id):
    if not is_admin(request):
        return redirect('signin')

    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    name = restaurant.name
    restaurant.delete()
    messages.info(request, f'Restaurant "{name}" deleted.')
    return redirect('admin_restaurants')

def admin_menu(request, restaurant_id):
    if not is_admin(request):
        return redirect('signin')

    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    context = get_common_context(request)
    context['restaurant'] = restaurant
    context['itemList'] = restaurant.items.all()
    return render(request, 'delivery/admin_menu.html', context)

def add_menu_item(request, restaurant_id):
    if not is_admin(request):
        return redirect('signin')

    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    context = get_common_context(request)
    context['restaurant'] = restaurant

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price = float(request.POST.get('price', 0))
        category = request.POST.get('category', 'Main Course').strip()
        vegeterian = request.POST.get('vegeterian') == 'on' or request.POST.get('vegeterian') == 'true'
        picture = request.POST.get('picture', '').strip()

        Item.objects.create(
            restaurant=restaurant,
            name=name,
            description=description or 'Delicious food prepared fresh.',
            price=price,
            category=category,
            vegeterian=vegeterian,
            picture=picture or 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600',
        )
        messages.success(request, f'Item "{name}" added to menu.')
        return redirect('admin_menu', restaurant_id=restaurant.id)

    return render(request, 'delivery/add_menu_item.html', context)

def update_menu_item(request, item_id):
    if not is_admin(request):
        return redirect('signin')

    item = get_object_or_404(Item, id=item_id)
    context = get_common_context(request)
    context['item'] = item

    if request.method == 'POST':
        item.name = request.POST.get('name', '').strip()
        item.description = request.POST.get('description', '').strip()
        item.price = float(request.POST.get('price', 0))
        item.category = request.POST.get('category', 'Main Course').strip()
        item.vegeterian = request.POST.get('vegeterian') == 'on' or request.POST.get('vegeterian') == 'true'
        item.picture = request.POST.get('picture', '').strip()
        item.save()

        messages.success(request, f'Item "{item.name}" updated.')
        return redirect('admin_menu', restaurant_id=item.restaurant.id)

    return render(request, 'delivery/edit_menu_item.html', context)

def delete_menu_item(request, item_id):
    if not is_admin(request):
        return redirect('signin')

    item = get_object_or_404(Item, id=item_id)
    restaurant_id = item.restaurant.id
    name = item.name
    item.delete()
    messages.info(request, f'Item "{name}" removed.')
    return redirect('admin_menu', restaurant_id=restaurant_id)

def admin_orders(request):
    if not is_admin(request):
        return redirect('signin')

    context = get_common_context(request)
    context['orders'] = Order.objects.order_by('-created_at')
    context['status_choices'] = ['Pending', 'Preparing', 'Out for Delivery', 'Delivered']
    return render(request, 'delivery/admin_orders.html', context)

def update_order_status(request, order_id):
    if not is_admin(request):
        return redirect('signin')

    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Preparing', 'Out for Delivery', 'Delivered']:
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to "{new_status}".')
    return redirect('admin_orders')