from .models import Purchase, Order


def count(request):
    if request.user.is_authenticated:
        cart_count = Purchase.objects.filter(user=request.user).count()
        orders_count = Order.objects.filter(user=request.user,details__has_paid=False
        ).distinct().count()
    else:
        cart_count = 0
        orders_count = 0

    return {'cart_count': cart_count, 'orders_count': orders_count}