from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),
    path('product/<int:id>',views.detail,name='detail'),
    path('createproduct',views.create_product,name='createproduct'),
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:id>', views.order_detail, name='order_detail'),
    path('editproduct/<int:id>', views.edit_product, name='editproduct'),
    path('deleteproduct/<int:id>', views.delete_product, name='deleteproduct'),
    path('register/',views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='myapp/logout.html'), name='logout'),
    path('invalid/',views.invalid, name='invalid'),
    path('cart/',views.my_purchases, name='my_purchases'),
    path('add-to-cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('submit-order/', views.submit_order, name='submit_order'),
    path('orders/<int:id>/pay/', views.pay_order, name='pay_order'),
    path('orders/detail/<int:id>/download/',views.download_product,name='download_product'),
    path('downloads/', views.my_downloads, name='my_downloads'),

]
