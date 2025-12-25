from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# USER ROLES
class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('CUSTOMER', 'Customer'),
        ('SELLER', 'Seller'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

# CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'

# PRODUCT
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'

# INVENTORY
class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.quantity

    class Meta:
        db_table = 'inventory'

# CART
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.cart

    class Meta:
        db_table = 'cart_item'

# ORDER
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'order'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.order

    class Meta:
        db_table = 'order_item'

# PAYMENT
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.order

    class Meta:
        db_table = 'payment'

# SHIPPING
class Shipping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.TextField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.order

    class Meta:
        db_table = 'shipping'