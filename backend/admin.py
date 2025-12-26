from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    User,
    Category,
    Product,
    Inventory,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Payment,
    Shipping,
    Review,
    Wishlist,
    Coupon,
    Notification
)

# --------------------------------------------------
# CUSTOM USER ADMIN
# --------------------------------------------------

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )


# --------------------------------------------------
# CATEGORY
# --------------------------------------------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# --------------------------------------------------
# PRODUCT & INVENTORY
# --------------------------------------------------

class InventoryInline(admin.StackedInline):
    model = Inventory
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'seller', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('name', 'seller__username')
    inlines = [InventoryInline]


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity')
    search_fields = ('product__name',)


# --------------------------------------------------
# CART & CART ITEM
# --------------------------------------------------

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username',)
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')
    search_fields = ('product__name',)


# --------------------------------------------------
# ORDER & ORDER ITEM
# --------------------------------------------------

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status')
    list_filter = ('status',)
    search_fields = ('user__username',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
    search_fields = ('product__name',)


# --------------------------------------------------
# PAYMENT
# --------------------------------------------------

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'payment_method', 'status')
    list_filter = ('status', 'payment_method')


# --------------------------------------------------
# SHIPPING
# --------------------------------------------------

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'status')
    list_filter = ('status',)


# --------------------------------------------------
# REVIEW
# --------------------------------------------------

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating')
    list_filter = ('rating',)
    search_fields = ('product__name', 'user__username')


# --------------------------------------------------
# WISHLIST
# --------------------------------------------------

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    search_fields = ('user__username', 'product__name')


# --------------------------------------------------
# COUPON
# --------------------------------------------------

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'discount', 'expiry_date')
    search_fields = ('code',)
    list_filter = ('expiry_date',)


# --------------------------------------------------
# NOTIFICATION
# --------------------------------------------------

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('user__username',)
