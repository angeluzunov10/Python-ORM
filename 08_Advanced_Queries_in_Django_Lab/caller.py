import os
import django
from django.db.models import Sum, Q, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct


def product_quantity_ordered():
    result = []

    orders = Product.objects.annotate(total=Sum('orderproduct__quantity')).values('name', 'total').order_by('-total')

    for order in orders:
        result.append(f"Quantity ordered of {order['name']}: {order['total']}")

    return '\n'.join(result)


def ordered_products_per_customer():
    result = []

    orders = Order.objects.prefetch_related('orderproduct_set__product__category').order_by('id')

    for o in orders:
        result.append(f"Order ID: {o.id}, Customer: {o.customer.username}")
        for ordered_product in o.orderproduct_set.all():
            result.append(f"- Product: {ordered_product.product.name}, Category: {ordered_product.product.category.name}")

    return '\n'.join(result)


def filter_products():
    result = []
    query = Q(price__gt=3.00) & Q(is_available=True)

    filtered_products = Product.objects.filter(query).order_by('-price', 'name')

    for p in filtered_products:
        result.append(f"{p.name}: {p.price}lv.")

    return "\n".join(result)


def give_discount():
    result = []

    query_for_reducing_price = Q(price__gt=3.00) & Q(is_available=True)

    products = Product.objects.filter(query_for_reducing_price).update(price=F('price') * 0.7)

    all_products = Product.objects.filter(is_available=True).order_by('-price', 'name')

    for p in all_products:
        result.append(f"{p.name}: {p.price}lv.")

    return "\n".join(result)


