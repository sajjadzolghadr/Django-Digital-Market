from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('product/<int:id>',views.detail,name='detail'),
    path("checkout/<int:id>", views.checkout, name="checkout"),
    path('createproduct',views.create_product,name='createproduct'),
    path('orders/', views.orders_list, name='orders_list'),
    path('editproduct/<int:id>', views.edit_product, name='editproduct'),
    path('deleteproduct/<int:id>', views.delete_product, name='deleteproduct'),
    path('register/',views.register, name='register'),

]
