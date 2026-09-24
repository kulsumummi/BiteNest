from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Customer(models.Model):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )
    
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Hashed password
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Restaurant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default="Delicious food served fresh every day.")
    cuisine = models.CharField(max_length=100)
    rating = models.FloatField(default=4.5)
    picture = models.URLField(max_length=500, default='https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, default="Fresh and delicious meal prepared with quality ingredients.")
    price = models.FloatField()
    category = models.CharField(max_length=50, default="Main Course")
    vegeterian = models.BooleanField(default=False)
    picture = models.URLField(max_length=500, default='https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&auto=format&fit=crop&q=80')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def subtotal(self):
        return round(self.item.price * self.quantity, 2)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cart")
    items = models.ManyToManyField(CartItem, related_name="carts")

    def total_price(self):
        return round(sum(cart_item.subtotal() for cart_item in self.items.all()), 2)

    def total_items(self):
        return sum(cart_item.quantity for cart_item in self.items.all())

    def __str__(self):
        return f"Cart for {self.customer.username}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.FloatField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    delivery_address = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username} (₹{self.total_amount})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()

    def subtotal(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f"{self.quantity} x {self.item_name} @ ₹{self.price}"