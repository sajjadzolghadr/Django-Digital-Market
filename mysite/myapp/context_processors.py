from .models import Purchase, Order,Notification
from django.db.models import Sum


def count(request):
    if request.user.is_authenticated:
        cart_count = Purchase.objects.filter(user=request.user).aggregate( total=Sum('quantity'))['total'] or 0
        orders_count = Order.objects.filter(customer__user=request.user).distinct().count()
        unread_notifications = Notification.objects.filter(user=request.user,is_read=False).count()
    else:
        cart_count = 0
        orders_count = 0
        unread_notifications = 0

    return {'cart_count': cart_count, 'orders_count': orders_count,'unread_notifications': unread_notifications}


def user_is_seller(request):
    if request.user.is_authenticated:
        return {
            'is_seller': request.user.groups.filter(
                name='seller'
            ).exists()
        }

    return {
        'is_seller': False
    }