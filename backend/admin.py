from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Shipping)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Coupon)
admin.site.register(Notification)
