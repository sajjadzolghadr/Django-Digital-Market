from django.shortcuts import render,get_object_or_404,redirect
from .forms import ProductForm, RegisterForm
from .models import Product,OrderDetail

# Create your views here.
def index(request):
    products = Product.objects.all()
    orders = OrderDetail.objects.all()
    return render(request, 'myapp/index.html', {'products': products,'orders': orders})

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
    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_product=form.save(commit=False)
            new_product.seller = request.user
            new_product.save()
            return redirect('index')
    else:
        form = ProductForm()

    return render(request, 'myapp/create_product.html', {'form': form})

def orders_list(request):
    orders = OrderDetail.objects.all().order_by('-created_on')
    return render(request, 'myapp/order_list.html', {'orders': orders})

def edit_product(request,id):
    product =Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES or None,instance=product)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductForm(instance=product)

    return render(request, 'myapp/edit_product.html', {'form': form, 'product': product})

def delete_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('index')

    return render(request, 'myapp/delete_product.html', {'product': product})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'myapp/register.html', {'form': form})
