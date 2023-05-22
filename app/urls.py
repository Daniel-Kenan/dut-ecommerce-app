from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_detail, name='products'), 
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<slug:slug>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<slug:slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/complete/', views.complete_order, name='complete_order'),
    path('order/history/', views.order_history, name='order_history'),
    path('shipping/address/', views.shipping_address, name='shipping_address'),
    path('search/', views.search, name='search'),
    # Authentication
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('category/<str:category>/', views.category_products, name='category_products'),
     path('payment/complete/', views.payment, name='payment_confirmation'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


