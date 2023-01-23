from django.contrib import admin
from django.urls import path, include
from .views import Index,signup, Login, logout,Cart, Checkout, ViewOrders
from store.middlewares.auth import auth_middleware


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('signup', signup, name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('cart', Cart.as_view(), name='cart'),
    path('checkout', auth_middleware(Checkout.as_view()), name='checkout'),
    path('orders', auth_middleware(ViewOrders.as_view()), name='orders'),
]
