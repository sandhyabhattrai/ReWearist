from django.urls import path
from . import views

urlpatterns = [
    
    path('categories/',views.get_all_categories,name="get-all-categories"),
    path('addcategory/',views.post_category,name="post-category"),
    path('deletecategory/<int:category_id>/',views.delete_category,name="delete-category"),
    path('updatecategory/<int:category_id>/',views.update_category,name="update-category"),

    path('allproducts',views.get_all_products,name="get-all-products"),
    path('addbook/',views.post_product,name="post-product"),
    path('deleteproduct/<int:product_id>/',views.delete_product,name="delete-product"),
    path('updateproduct/<int:product_id>/',views.update_product,name="update-product"),

    path('dashboard/',views.admin_dashboard,name="admin-dashboard"),
    path('allorders/',views.all_orders,name="all-orders"),
    path('customers/',views.customers,name="customers"),
]