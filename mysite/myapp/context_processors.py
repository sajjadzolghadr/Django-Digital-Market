from .models import Purchase

def cart_count(request):
    if request.user.is_authenticated:
        count = Purchase.objects.filter(user=request.user).count()
    else:
        count = 0

    return {'cart_count': count}