from django.contrib import admin
from .models import Category, Product, Wishlist, Order, OrderItem, ShippingAddress,Driver


admin.site.site_title = "DUT Ecommerce Admin"
admin.site.title = "DUT Ecommerce Admin"
admin.site.site_title = "DUT Ecommerce Admin"
admin.site.index_title = "DUT Ecommerce Admin"
admin.site.site_header = "DUT Ecommerce Admin"

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Driver)