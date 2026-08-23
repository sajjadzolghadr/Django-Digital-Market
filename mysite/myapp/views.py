from django.shortcuts import render,get_object_or_404
from .forms import ProductForm
from .models import Product,OrderDetail

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'myapp/index.html', {'products': products})

def detail(request,id):
    product = Product.objects.get(id=id)
    return render(request, 'myapp/detail.html', {'product': product})

def checkout(request,id):
    product = get_object_or_404(Product,id=id)
    order=OrderDetail.objects.create(
        customer_email=request.user.email,
        product=product,
        amount=product.price,
        stripe_payment_id="",
        has_paid=False,
    )
    return render(request, 'myapp/checkout.html', {'order': order, 'product': product})

def create_product(request):
    form = ProductForm(request.POST or None)
    return render(request, 'myapp/create_product.html', {'form': form})