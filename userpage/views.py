
from django.shortcuts import render,redirect
from wearist.models import Products
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Cart,Order, Products
from django.contrib import messages
from accounts.auth import user_only
from .forms import OrderForm, LocationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import UserProfile
from math import radians, sin, cos, sqrt, atan2

# Create your views here.


def homepage(request):
    products = Products.objects.all().order_by('-id')[:4]
    return render(request,'client/homepage.html',{
        'products': products
    })

def productpage(request):
    products = Products.objects.all().order_by('-created_at')
    return render(request,'client/productpage.html',{'products':products})

def product_details(request, product_id):
    product = Products.objects.get(id=product_id)
    return render(request,'client/productdetail.html',{'product':product})


# add to cart
@login_required
@user_only
def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Products, id=product_id)

    check_product_presence = Cart.objects.filter(user=user, product=product)

    if check_product_presence.exists():
        messages.error(request, 'This item is already in your cart')
        return redirect('/products/')
    else:
        cart = Cart.objects.create(user=user, product=product)
        if cart:
            messages.success(request, 'Item added to cart successfully')
            return redirect('/cart/')
        else:
            messages.error(request, 'Failed to add this item to cart')
            return redirect('/products/')


@login_required
@user_only       
def cart_page(request):
    user = request.user
    carts = Cart.objects.filter(user = user)
    return render(request,'client/cart.html',{'carts':carts})
        


# delete from cart 
@login_required
@user_only
def delete_from_cart(request, cart_id):
    user = request.user
    cart = Cart.objects.filter(user = user ,id = cart_id)
    cart.delete()
    messages.add_message(request,messages.SUCCESS,'Item removed from cart successfully. ')
    return redirect('/cart/')

@login_required
@user_only
def user_order(request,cart_id,product_id):
    user = request.user
    product = Products.objects.get(id = product_id)
    cart = Cart.objects.get(id = cart_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            quantity = data['quantity']
            price = product.price
            total_price = int(quantity) * int(price)
            payment_method = data['payment_method']
            contact_no = data['contact_no']
            address = data['address']

            order = Order.objects.create(
                product = product,
                user = user,
                quantity = quantity,
                total_price = total_price,
                payment_method = payment_method,
                contact_no = contact_no,
                address = address
            )

            if order.payment_method == 'Cash on Delivery':
                cart.delete()
                messages.add_message(request,messages.SUCCESS,'Order placed successfully.')
                return redirect('/myorders')
        else:
            messages.add_message(request,messages.ERROR,'Order Failed')
            return render(request,'client/orderform.html',{'form':form})
    return render(request,'client/orderform.html',{'form':OrderForm})



@login_required
@user_only
def show_myorder(request):
    user = request.user
    orders = Order.objects.filter(user = user)
    return render(request,'client/myorders.html',{'orders':orders})


@login_required
@user_only
def mark_as_deliver(request,order_id):
    order = Order.objects.get(id = order_id)
    order.status = 'Delivered...'
    order.save()
    messages.add_message(request,messages.SUCCESS,'Order marked as delivered.')
    return redirect('/myorders')

def pricing(request):
    return render(request, 'client/pricing.html')

def faq(request):
    return render(request, 'client/faq.html')

def about(request):
    return render(request, 'client/about.html')


@login_required
def update_location(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        form = LocationForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Location updated.")
            return redirect('seller-map')
    else:
        form = LocationForm(instance=profile)

    return render(request, 'client/location_update.html', {'form': form})



def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


@login_required
def seller_map(request):
    current_user = request.user


    try:
        current_profile = current_user.userprofile
    except UserProfile.DoesNotExist:
        current_profile = UserProfile.objects.create(user=current_user)

    all_users = UserProfile.objects.exclude(user=current_user).exclude(latitude=None)

    users_with_distance = []
    for u in all_users:
        if u.latitude is not None and u.longitude is not None and \
        current_profile.latitude is not None and current_profile.longitude is not None:
        
            distance = haversine(
                current_profile.latitude,
                current_profile.longitude,
                u.latitude,
                u.longitude
            )

            users_with_distance.append({
                'name': u.user.username,
                'lat': u.latitude,
                'lng': u.longitude,
                'distance': round(distance, 2),
                'address': u.address,
            })


    return render(request, 'client/seller_map.html', {
        'users': users_with_distance,
        'my_lat': current_profile.latitude,
        'my_lng': current_profile.longitude,
    })

