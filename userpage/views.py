from django.shortcuts import render,redirect
from wearist.models import Products
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Cart,Order
from django.contrib import messages
from accounts.auth import user_only
from .forms import OrderFrom
from django.contrib import messages

# Create your views here.


def homepage(request):
    products = Products.objects.all().order_by('-id')[:8]
    return render(request,'client/homepage.html',{
        'products': products
    })

def productpage(request):
    products = Products.objects.all().order_by('-created_at')
    return render(request,'client/productpage.html',{'products':products})

def product_details(request, product_id):
    product = Products.objects.get(id=product_id)
    return render(request,'client/detail.html',{'product':product})


# add to cart
@login_required
@user_only
def add_to_cart(request,product_id):
    user = request.user
    product = Products.objects.get(id = product_id)

    check_product_presence = Cart.objects.filter(user = user, product= product)

    if check_product_presence:
        messages.add_message(request,messages.ERROR,'This item is already in your cart')
        return redirect('/products/')
    else:
        cart = Cart.objects.create(user = user,product = product)
        if cart:
            messages.add_message(request,messages.SUCCESS,'Item added to cart successfully')
            return redirect('/cart/')
        else:
            messages.add_message(request,messages.ERROR,'Failed to add this item to cart')
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
def delete_from_cart(request, product_id):
    user = request.user
    cart = Cart.objects.filter(user = user ,id = product_id)
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
        form = OrderFrom(request.POST)
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
    return render(request,'client/orderform.html',{'form':OrderFrom})


@login_required
@user_only
def show_myorder(request):
    user = request.user
    orders = Order.objects.filter(user = user)
    return render(request,'client/myorder.html',{'orders':orders})


@login_required
@user_only
def mark_as_deliver(request,order_id):
    order = Order.objects.get(id = order_id)
    order.status = 'Delivered...'
    order.save()
    messages.add_message(request,messages.SUCCESS,'Order marked as delivered.')
    return redirect('/myorders')
