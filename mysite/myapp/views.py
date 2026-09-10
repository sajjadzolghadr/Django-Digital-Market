from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum , Q
from django.shortcuts import render,get_object_or_404,redirect
from .forms import ProductForm, RegisterForm
from .models import Product, OrderDetail, Purchase, Order, Customer, Wishlist
from django.http import FileResponse
# Create your views here.
def index(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', '')
    products = Product.objects.select_related('seller').all()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    if sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'oldest':
        products = products.order_by('created_at')
    elif sort == 'cheap':
        products = products.order_by('price')
    elif sort == 'expensive':
        products = products.order_by('-price')
    orders = Order.objects.select_related('customer').all()
    customers = Customer.objects.select_related('user').all()
    seller_products = products
    seller_orders = orders
    if request.user.is_authenticated and request.user.groups.filter(name='seller').exists():
        seller_products = Product.objects.filter(seller=request.user)
        seller_orders = Order.objects.filter(details__product__seller=request.user).distinct()
    total_sales = OrderDetail.objects.filter(product__seller=request.user,has_paid=True).aggregate(total=Sum('amount'))['total'] or 0
    latest_product = Product.objects.order_by('-id').first()
    latest_order = Order.objects.order_by('-id').first()
    latest_user = User.objects.order_by('-id').first()
    return render(request, 'myapp/index.html', {'products': products,'orders': orders,'total_sales': total_sales,'latest_product': latest_product, 'latest_order': latest_order, 'latest_user': latest_user,'customers': customers,'seller_products': seller_products,'seller_orders': seller_orders,'query': query,'sort': sort,})

def detail(request,id):
    product = Product.objects.get(id=id)
    return render(request, 'myapp/detail.html', {'product': product})


def create_product(request):
    if not request.user.groups.filter(name='seller').exists():
        return redirect('invalid')
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

@login_required
def orders_list(request):
    orders = Order.objects.filter(
        customer__user=request.user
    ).prefetch_related('details').order_by('-created_at')

    return render(request, 'myapp/order_list.html', {
        'orders': orders
    })
@login_required
def order_detail(request, id):
    order = get_object_or_404(
        Order,
        id=id,
        customer__user=request.user
    )

    details = OrderDetail.objects.filter(order=order)

    return render(request, 'myapp/order_detail.html', {
        'order': order,
        'details': details
    })

def edit_product(request,id):
    product =Product.objects.get(id=id)
    if product.seller != request.user:
        return redirect('invalid')
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
    if product.seller != request.user:
        return redirect('invalid')
    if request.method == 'POST':
        product.delete()
        return redirect('index')

    return render(request, 'myapp/delete_product.html', {'product': product})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'myapp/register.html', {'form': form})


def invalid(request):
    return render(request, 'myapp/invalid.html')

@login_required
def add_to_cart(request, id):
    product = Product.objects.get(id=id)

    Purchase.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('index')

@login_required
def my_purchases(request):
    purchases = Purchase.objects.filter(user=request.user)
    total = sum(p.product.price for p in purchases)
    return render(request, 'myapp/my_purchases.html', {'purchases': purchases,'total': total})

@login_required
def submit_order(request):
    if request.method == 'POST':
        purchases = Purchase.objects.filter(user=request.user)
        customer = get_object_or_404(Customer,user=request.user)

        if purchases.exists():
            order = Order.objects.create(customer=customer)

            for purchase in purchases:
                OrderDetail.objects.create(
                    order=order,
                    product=purchase.product,
                    amount=purchase.product.price,
                    has_paid=False
                )

            purchases.delete()

        return redirect('orders_list')

    return redirect('my_purchases')

@login_required
def pay_order(request, id):
    order = get_object_or_404(
        Order,
        id=id,
        customer__user=request.user
    )

    if request.method == 'POST':
        OrderDetail.objects.filter(order=order).update(
            has_paid=True
        )

        return redirect('order_detail', id=order.id)

    return redirect('order_detail', id=order.id)

@login_required
def download_product(request, id):
    detail = get_object_or_404(
        OrderDetail,
        id=id,
        order__customer__user=request.user,
        has_paid=True
    )

    product = detail.product

    if not product.file:
        return redirect('invalid')

    return FileResponse(
        product.file.open('rb'),
        as_attachment=True,
        filename=product.file.name.split('/')[-1]
    )

@login_required
def my_downloads(request):
    downloads = OrderDetail.objects.filter(
        order__customer__user=request.user,
        has_paid=True
    ).select_related('product', 'order')

    return render(request, 'myapp/my_downloads.html', { 'downloads': downloads})


@login_required
def sales_history(request):
    if not request.user.groups.filter(name='seller').exists():
        return redirect('invalid')

    orders = Order.objects.filter(
        details__product__seller=request.user,
        details__has_paid=True
    ).distinct().prefetch_related('details__product').order_by('-created_at')

    for order in orders:
        order.seller_total = sum(
            detail.amount
            for detail in order.details.all()
            if detail.product.seller == request.user
            and detail.has_paid
        )

    return render(request, 'myapp/sales_history.html', {
        'orders': orders
    })

@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    customer = get_object_or_404(Customer, user=request.user)

    Wishlist.objects.get_or_create(
        customer=customer,
        product=product
    )

    return redirect('index')

@login_required
def my_wishlist(request):
    customer = get_object_or_404(
        Customer,
        user=request.user
    )

    wishlist = Wishlist.objects.filter(
        customer=customer
    ).select_related('product')

    return render(request, 'myapp/wishlist.html', {
        'wishlist': wishlist
    })


@login_required
def remove_from_wishlist(request, id):
    customer = get_object_or_404(Customer, user=request.user)

    wishlist = get_object_or_404(
        Wishlist,
        id=id,
        customer=customer
    )

    wishlist.delete()

    return redirect('my_wishlist')