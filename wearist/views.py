from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from . models import Products,Category
from .forms import CategoryForm,ProductForm
from django.contrib.auth.decorators import login_required
from accounts.auth import admin_only
from userpage.models import Order
from django.contrib.auth.models import User


@login_required
@admin_only
def get_all_categories(request):
    all_categories = Category.objects.all()
    return render(request,"wearist/category/allcategories.html",{
        'categories': all_categories
    })

@login_required
@admin_only
def post_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,"Category added successfully")
            return redirect("/admin/categories/")
        else:
            messages.add_message(request,messages.ERROR,"Failed to add category")
            return render(request,"wearist/category/postcategory.html",{'form': form})
    
    return render(request,"wearist/category/postcategory.html",{
        'form': CategoryForm
    })

@login_required
@admin_only
def delete_category(request,category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    messages.add_message(request,messages.SUCCESS,"Category deleted successfully")
    return redirect("/admin/categories/")


@login_required
@admin_only
def update_category(request,category_id):
    category = Category.objects.get(id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,"Category updated successfully")
            return redirect("/admin/categories/")
        else:
            messages.add_message(request,messages.ERROR,"Failed to update category")
            return render(request,"wearist/category/updatecategory.html",{'form': form})
    return render(request,"wearist/category/updatecategory.html",{

        'form': CategoryForm(instance=category)
    }
)

@login_required
@admin_only
def get_all_products(request):
    all_products = Products.objects.all()
    return render(request,"/products/allproducts.html",{
        'products': all_products
    })

@login_required
@admin_only
def post_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Product Added Successfully')
            return redirect('/admin/allproducts') #http://localhost:8000/books
        else:
            messages.add_message(request,messages.ERROR,'Failed to Add product')
            return render(request,'wearist/products/postproduct.html',{'form': form})
        
    return render(request,"wearist/product/postproduct.html",{
        'form': ProductForm
    }
    )

@login_required
@admin_only
def delete_product(request,product_id):
    book = Products.objects.get(pk=product_id)
    book.delete()
    messages.add_message(request,messages.SUCCESS,'Product Deleted Successfully')
    return redirect('/admin/allproducts')

@login_required
@admin_only
def update_product(request,product_id):
    product = Products.objects.get(pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Product Updated Successfully')
            return redirect('/admin/allproducts')
        else:
            messages.add_message(request,messages.ERROR,'Failed to Update product.')
            return render(request,'wearist/products/updateproduct.html',{'form': form})
    return render(request,'wearist/products/updateproduct.html',{
        'form': ProductForm(instance=product)
    })



@login_required
@admin_only
def admin_dashboard(request):
    orders = Order.objects.filter(status = 'Delivered...')
    users = User.objects.all()
    books = Products.objects.filter(instock = True)
    pending_products = Order.objects.filter(status = 'Pending...')
    categories = Category.objects.all()
    return render(request,"wearist/dashboard/dashboard.html",{
        'total_delivered': len(orders),
        'total_users': len(users),
        'total_books': len(books),
        'pending_books': len(pending_products),
        'total_categories': len(categories),
    })


@login_required
@admin_only
def all_orders(request):
    orders = Order.objects.all()
    context = {
        'orders': orders
    }
    return render(request,"wearist/dashboard/orders.html",context)

@login_required
@admin_only
def customers(request):
    customers = User.objects.all()
    context = {
        'users': customers
    }
    return render(request,"wearist/dashboard/customers.html",context)