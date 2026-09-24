from django.urls import path
from . import views

urlpatterns = [
    # Public & Auth
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),

    # Customer
    path('restaurants/', views.restaurants, name='restaurants'),
    path('menu/<int:restaurant_id>/', views.view_menu, name='view_menu'),
    path('cart/', views.show_cart, name='show_cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:cart_item_id>/', views.remove_item, name='remove_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.orders, name='orders'),

    # Admin
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/restaurants/', views.admin_restaurants, name='admin_restaurants'),
    path('admin-panel/restaurants/add/', views.add_restaurant, name='add_restaurant'),
    path('admin-panel/restaurants/edit/<int:restaurant_id>/', views.update_restaurant, name='update_restaurant'),
    path('admin-panel/restaurants/delete/<int:restaurant_id>/', views.delete_restaurant, name='delete_restaurant'),
    path('admin-panel/menu/<int:restaurant_id>/', views.admin_menu, name='admin_menu'),
    path('admin-panel/menu/add/<int:restaurant_id>/', views.add_menu_item, name='add_menu_item'),
    path('admin-panel/menu/edit/<int:item_id>/', views.update_menu_item, name='update_menu_item'),
    path('admin-panel/menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('admin-panel/orders/', views.admin_orders, name='admin_orders'),
    path('admin-panel/orders/update_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
]
