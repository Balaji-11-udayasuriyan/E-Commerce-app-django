from django.urls import path
from . import views

urlpatterns = [

    # -----------------------------
    # AUTHENTICATION
    # -----------------------------
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # -----------------------------
    # HOME & PRODUCTS
    # -----------------------------
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # -----------------------------
    # SELLER
    # -----------------------------
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/add-product/', views.add_product, name='add_product'),

    # -----------------------------
    # CART
    # -----------------------------
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # -----------------------------
    # ORDERS
    # -----------------------------
    path('order/place/', views.place_order, name='place_order'),
    path('orders/', views.orders, name='orders'),

    # -----------------------------
    # PAYMENT & SHIPPING
    # -----------------------------
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),

    # -----------------------------
    # WISHLIST
    # -----------------------------
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),

    # -----------------------------
    # REVIEWS
    # -----------------------------
    path('review/add/<int:product_id>/', views.add_review, name='add_review'),

    # -----------------------------
    # ADMIN
    # -----------------------------
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
