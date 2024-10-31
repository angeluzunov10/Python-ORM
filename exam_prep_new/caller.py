import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here


from main_app.models import Profile, Order, Product
from django.db.models import Q, Count, F, Case, When, Value, BooleanField


# Task 4

def get_profiles(search_string=None):
    if search_string is None:
        return ""

    result = []

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
            |
        Q(email__icontains=search_string)
            |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not profiles.exists():
        return ""

    for p in profiles:
        result.append(f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders.count()}")

    return "\n".join(result)


def get_loyal_profiles():
    result = []

    loyal_profiles = Profile.objects.get_regular_customers()
    if not loyal_profiles.exists():
        return ""

    for p in loyal_profiles:
        result.append(f"Profile: {p.full_name}, orders: {p.orders.count()}")

    return "\n".join(result)


def get_last_sold_products():
    last_order = Order.objects.prefetch_related('products').last()

    if last_order is None or not last_order.products.exists():
        return ''

    products = ', '.join([p.name for p in last_order.products.order_by('name')])

    # products = ', '.join(last_order.products.order_by(name).values_list('name', flat=True))

    return f"Last sold products: {products}"


# Task 5

def get_top_products():
    top_products = Product.objects.annotate(
        times_sold=Count('order')  # here I am connecting the class Order
    ).filter(
        times_sold__gt=0
    ).order_by(
        '-times_sold', 'name'
    )[:5]

    if not top_products.exists():
        return ""

    product_lines = '\n'.join(f"{p.name}, sold {p.times_sold} times" for p in top_products)

    return "Top products:\n" + product_lines


def apply_discounts():
    not_completed_products = Order.objects.annotate(
        products_count=Count('products')
    ).filter(
        products_count__gt=2,
        is_completed=False
    )

    if not not_completed_products.exists():
        return "Discount applied to 0 orders."

    not_completed_products.update(total_price=0.9 * F('total_price'))

    return f"Discount applied to {not_completed_products.count()} orders."


def complete_order():
    oldest_order = Order.objects.filter(
        is_completed=False
    ).order_by(
        'creation_date'
    ).first()

    if not oldest_order:
        return ""

    # for p in oldest_order.products.all():
    #     p.in_stock -= 1
    #
    #     if p.in_stock == 0:
    #         p.is_available = False
    #
    #     p.save()

    oldest_order.products.update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available'),
            output_field=BooleanField()
        )
    )

    oldest_order.is_completed = True
    oldest_order.save()

    return "Order has been completed!"
