from django.contrib import admin
from .models import Product,OrderDetail,Order,Customer
# Register your models here.
admin.site.register(Product)
admin.site.register(OrderDetail)
admin.site.register(Order)
admin.site.register(Customer)