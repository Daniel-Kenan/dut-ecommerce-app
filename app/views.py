from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Wishlist, Order, OrderItem, ShippingAddress
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from random import shuffle
from django.shortcuts import render
from .forms import SearchForm
from .models import Product
from .forms import DriverSignUpForm

from django import forms
from django.contrib.auth.forms import UserCreationForm


from django.http import FileResponse
from django.conf import settings
import os

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import DriverRegistrationForm


def download_db(request):
    db_file = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    return FileResponse(open(db_file, 'rb'), as_attachment=True)

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


def category_products(request, category):
    category = get_object_or_404(Category, name=category)
    products = Product.objects.filter(category=category, available=True)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'category_products.html', context)



def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    products = list(products)
    for product in products:
        product.original = product.price + random.randint(5,150)
    shuffle(products)
    context = {
        'categories': categories,
        'products': products,
        
    }
    return render(request, 'home.html', context)


@login_required
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)
from django.contrib import messages

@login_required
def add_to_wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, "Product added to wishlist.")
    else:
        messages.warning(request, "Product already in wishlist.")
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.product.remove(product)
    return render(request, 'wishlist.html', {'wishlist': wishlist})


@login_required
def wishlist(request):
    try:
        wishlist = Wishlist.objects.filter(user=request.user)
        tmp = []
        for wish in wishlist: 
          tmp.append(wish.product)
        
    except Wishlist.DoesNotExist:
        wishlist = None
   
    context = {
        'wishlist': tmp
    }
    
    return render(request, 'wishlist.html', context)


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'quantity': 1})

    if not item_created:
        # Update the quantity if the order item already exists
        order_item.quantity += 1
        order_item.save()

    return render(request, 'cart.html', {'order': order})


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order = get_object_or_404(Order, user=request.user, is_completed=False)
    order_item = get_object_or_404(OrderItem, order=order, product=product)
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order_item.delete()
    return render(request, 'cart.html', {'order': order})


@login_required
def cart_view(request):
    try:
        order = Order.objects.get(user=request.user, is_completed=False)
        order_items = OrderItem.objects.filter(order=order)
        context = {
            'order': order,
            'order_items': order_items,
        }
    except Order.DoesNotExist:
        context = {
            'order': None,
            'order_items': None,
        }
    return render(request, 'cart.html', context)


from email.message import EmailMessage
import smtplib
import ssl
import time
from datetime import datetime,timedelta
import random
@login_required
def complete_order(request):
    order = get_object_or_404(Order, user=request.user, is_completed=False)
    # order.is_completed = True
    # order.save()
    product_names = order.products.values_list('name', flat=True)
    price = order.products.values_list('price', flat=True)
    price = list(map(lambda x: str(x), price))
    price = eval("+".join(price))

    product_names = list(product_names)
    product_names =",".join(product_names)
    if order.is_completed:
        msg = EmailMessage()
        msg['Subject'] = "order confirmation"
        msg['From'] = "botauto212@gmail.com"
        msg['To'] = request.user.email
        msg.set_content("Email From: " + "\n\nMessage:\n" + "Order confirmed of item(s): "+product_names+"\nOrder number: " +str(int(order.created_at.timestamp())) + "\nPayment: R"+str(price) )
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
          smtp.login(msg['From'],"cjeifgsiqfivevdx")
          smtp.sendmail(msg["From"],msg["To"],msg.as_string())
    return render(request, 'order_confirmation.html', {'order': str(int(order.created_at.timestamp())), 'price':price,'user':request.user.username,'email':request.user.email})


@login_required
def payment(request):
    request.POST.get('email')
    order = get_object_or_404(Order, user=request.user, is_completed=False)
    order.is_completed = True
    order.save()
    product_names = order.products.values_list('name', flat=True)
    price = order.products.values_list('price', flat=True)
    price = list(map(lambda x: str(x), price))
    price = eval("+".join(price))
    product_names = list(product_names)
    product_names =",".join(product_names)
    days =random.randint(1,30)
    current_date = datetime.now()
    future_date = current_date + timedelta(days=days)
    future_date_string = future_date.strftime("%Y-%m-%d")
    
    if order.is_completed:
        msg = EmailMessage()
        msg['Subject'] = "order confirmation"
        msg['From'] = "botauto212@gmail.com"
        msg['To'] = request.POST.get('email')
        msg.set_content("Email From: " + "\n\nMessage:\n" + "Order confirmed of item(s): "+product_names+"\nOrder number: " +str(int(order.created_at.timestamp())) + "\nPayment: R "+str(price)+ "\nYour Package will be delivered in "+ str(days)+ " days"+ " which will be on "+ future_date_string )
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
          smtp.login(msg['From'],"cjeifgsiqfivevdx")
          smtp.sendmail(msg["From"],msg["To"],msg.as_string())
    return render(request, 'billing.html', {'order': str(int(order.created_at.timestamp())), 'price':price,'user':request.user.username, 'email':request.user.email})





@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})


@login_required
def shipping_address(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        shipping_address, created = ShippingAddress.objects.get_or_create(user=request.user)
        shipping_address.address = address
        shipping_address.city = city
        shipping_address.postal_code = postal_code
        shipping_address.save()
        return render(request, 'shipping_address.html', {'shipping_address': shipping_address})
    else:
        shipping_address = get_object_or_404(ShippingAddress, user=request.user)
        return render(request, 'shipping_address.html', {'shipping_address': shipping_address})
    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired redirect URL after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')



def search(request):
    form = SearchForm(request.GET)
    query = form['query'].value() if form.is_valid() else ''
    results = Product.objects.filter(name__icontains=query)
    context = {
        'form': form,
        'query': query,
        'results': results,
    }
    return render(request, 'search_results.html', context)

from .forms import DriverRegistrationForm
from .models import Delivery
def driver_registration(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = DriverRegistrationForm()
    return render(request, 'driver_registration.html', {'form': form})

# @login_required
# def driver_deliveries(request):
#     driver = request.user.driver  # Assuming the driver is authenticated
#     deliveries = Delivery.objects.filter(driver=driver)
    
#     if request.method == 'POST':
#         delivery_id = request.POST.get('delivery_id')
#         delivery_status = request.POST.get('delivery_status')
#         delivery = Delivery.objects.get(pk=delivery_id)
#         delivery.delivery_status = delivery_status
#         delivery.save()
    
#     context = {
#         'deliveries': deliveries
#     }
#     return render(request, 'driver_deliveries.html', context)

@login_required
def driver_deliveries(request):
    # Get all orders assigned to the driver
    driver_orders = Order.objects.filter(driver=request.user.driver)
    context = {
        'orders': driver_orders
    }
    return render(request, 'driver_deliveries.html', context)

def update_delivery_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        delivery_status = request.POST.get('delivery_status')
        order.delivery_status = delivery_status
        order.save()    
        return redirect('driver_deliveries')
    
    context = {
        'order': order
    }
    return render(request, 'update_delivery_status.html', context)


def driver_register(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log in the user
            login(request, user)
            return redirect('driver_dashboard')  # Replace 'driver_dashboard' with your desired redirect URL after successful registration
    else:
        form = DriverRegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'driver_register.html', context)


@login_required
def driver_dashboard(request):
    return render(request, 'driver_dashboard.html')

# def driver_signup(request):
#     if request.method == 'POST':
#         form = DriverSignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Additional logic to assign driver role to the user if necessary
#             return redirect('login')  # Redirect to the login page
#     else:
#         form = DriverSignUpForm()
#     return render(request, 'driver_signup.html', {'form': form})