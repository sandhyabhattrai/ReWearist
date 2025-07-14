from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('products/',views.productpage,name='productpage'),
    path('products/<int:product_id>/',views.product_details,name='product-details'),
    path('addtocart/<int:product_id>/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.cart_page,name='cart'),
    path('cart/<int:cart_id>',views.delete_from_cart,name='delete-from-cart'),
    path('order/<int:cart_id>/<int:product_id>/',views.user_order,name='user-order'),
    path('myorders/',views.show_myorder,name='myorders'),
    path('markasdeliver/<int:order_id>/',views.mark_as_deliver,name='mark-as-deliver'),
    path('pricing/', views.pricing, name='pricing'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('update-location/', views.update_location, name='update-location'),
    path('user-map/', views.seller_map, name='seller-map'),
]