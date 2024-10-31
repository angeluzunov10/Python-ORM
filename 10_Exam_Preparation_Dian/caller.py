import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Profile, Order
from django.db.models import Q


# Create queries within functions


def get_profiles(search_string=None):
    if search_string is None:
        return ""

    result = []

    matching_profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string) |
        Q(email__icontains=search_string) |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not matching_profiles.exists():
        return ""

    for p in matching_profiles:
        result.append(f"Profile: {p.full_name},"
                      f" email: {p.email},"
                      f" phone number: {p.phone_number},"
                      f" orders:{p.profile_orders.count()}")

    return "\n".join(result)


def get_loyal_profiles():
    result = []

    loyal_profiles = Profile.objects.get_regular_customers()
    if not loyal_profiles.exists():
        return ""

    for p in loyal_profiles:
        result.append(f"Profile: {p.full_name}, orders: {p.profile_orders.count()}")

    return "\n".join(result)


def get_last_sold_products():
    last_order = Order.objects.prefetch_related('products').last()

    if last_order is None or not last_order.products.exists():
        return ''

    products = ', '.join([p.name for p in last_order.products.order_by('name')])

    # products = ', '.join(last_order.products.order_by(name).values_list('name', flat=True))

    return f"Last sold products: {products}"
