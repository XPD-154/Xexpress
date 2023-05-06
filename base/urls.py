from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('product/', views.product, name='product'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('sign_up/', views.sign_up_pg, name='sign_up_pg'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login_pg, name='login_pg'),
]
