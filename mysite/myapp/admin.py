from django.contrib import admin
from .models import Product,OrderDetail,Order,Customer,Review,Category
# Register your models here.
admin.site.register(Product)
admin.site.register(OrderDetail)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Review)
admin.site.register(Category)