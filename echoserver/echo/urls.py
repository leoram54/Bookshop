from django.urls import path
from .views import *


urlpatterns = [
    path('', book_list, name='book_list'),
    path('new/', book_create, name='book_create'),
    path('<int:pk>/edit/', book_update, name='book_update'),
    path('book/<int:pk>/delete/', book_delete, name='book_delete'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('add_to_cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_history, name='order_history'),
    path('check_username/', check_username, name='check_username'),
]