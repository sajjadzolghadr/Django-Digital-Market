from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),
    path('product/<int:id>',views.detail,name='detail'),
    path("checkout/<int:id>", views.checkout, name="checkout"),
    path('createproduct',views.create_product,name='createproduct'),
    path('orders/', views.orders_list, name='orders_list'),
    path('editproduct/<int:id>', views.edit_product, name='editproduct'),
    path('deleteproduct/<int:id>', views.delete_product, name='deleteproduct'),
    path('register/',views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),

]
