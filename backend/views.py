from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum

from backend.models import Product, Category, Review, Inventory, Cart, CartItem, Order, OrderItem, Payment, Shipping, \
    Wishlist, User


# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# --------------------------------------------------
# HOME & PRODUCTS
# --------------------------------------------------

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "home.html", {
        "products": products,
        "categories": categories
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, "product_detail.html", {
        "product": product,
        "reviews": reviews
    })


# --------------------------------------------------
# SELLER VIEWS
# --------------------------------------------------

@login_required
def seller_dashboard(request):
    if request.user.role != "SELLER":
        return redirect("home")

    products = Product.objects.filter(seller=request.user)
    return render(request, "seller/dashboard.html", {"products": products})


@login_required
def add_product(request):
    if request.user.role != "SELLER":
        return redirect("home")

    if request.method == "POST":
        product = Product.objects.create(
            seller=request.user,
            name=request.POST["name"],
            price=request.POST["price"],
            stock=request.POST["stock"],
            category_id=request.POST["category"],
            description=request.POST["description"]
        )
        Inventory.objects.create(product=product, quantity=product.stock)
        return redirect("seller_dashboard")

    categories = Category.objects.all()
    return render(request, "seller/add_product.html", {"categories": categories})


# --------------------------------------------------
# CART
# --------------------------------------------------

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
    item.save()

    return redirect("cart")


@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, "cart.html", {
        "items": items,
        "total": total
    })


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect("cart")


# --------------------------------------------------
# ORDERS
# --------------------------------------------------

@login_required
def place_order(request):
    cart = Cart.objects.filter(user=request.user).first()
    items = CartItem.objects.filter(cart=cart)

    if not items:
        return redirect("cart")

    total = sum(item.product.price * item.quantity for item in items)

    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        status="Pending"
    )

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

        item.product.stock -= item.quantity
        item.product.save()

    items.delete()
    return redirect("orders")


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders.html", {"orders": orders})


# --------------------------------------------------
# PAYMENT & SHIPPING
# --------------------------------------------------

@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    Payment.objects.create(
        order=order,
        payment_method="ONLINE",
        status="SUCCESS"
    )

    Shipping.objects.create(
        order=order,
        address="Default Address",
        status="Processing"
    )

    order.status = "Confirmed"
    order.save()

    return redirect("orders")


# --------------------------------------------------
# WISHLIST
# --------------------------------------------------

@login_required
def add_to_wishlist(request, product_id):
    Wishlist.objects.get_or_create(
        user=request.user,
        product_id=product_id
    )
    return redirect("wishlist")


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, "wishlist.html", {"items": items})


# --------------------------------------------------
# REVIEWS
# --------------------------------------------------

@login_required
def add_review(request, product_id):
    if request.method == "POST":
        Review.objects.create(
            product_id=product_id,
            user=request.user,
            rating=request.POST["rating"],
            comment=request.POST["comment"]
        )
    return redirect("product_detail", product_id=product_id)


# --------------------------------------------------
# ADMIN DASHBOARD
# --------------------------------------------------

@login_required
def admin_dashboard(request):
    if request.user.role != "ADMIN":
        return redirect("home")

    total_users = User.objects.count()
    total_orders = Order.objects.count()
    revenue = Order.objects.aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    return render(request, "admin/dashboard.html", {
        "users": total_users,
        "orders": total_orders,
        "revenue": revenue
    })
