from django.contrib import admin
from .models import Customer, Restaurant, Item, Cart, CartItem, Order, OrderItem

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile', 'role', 'created_at')
    list_filter = ('role',)
    search_fields = ('username', 'email', 'mobile')

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuisine', 'rating', 'created_at')
    search_fields = ('name', 'cuisine')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'category', 'vegeterian')
    list_filter = ('restaurant', 'category', 'vegeterian')
    search_fields = ('name', 'category')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'quantity')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username', 'delivery_address', 'contact_phone')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'item_name', 'quantity', 'price')