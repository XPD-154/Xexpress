from django.shortcuts import render
from .models import *               #import all models into view

# Create your views here.
def index(request):
    products = Product.objects.all().order_by('id')[:3]
    context = {'products':products}
    return render(request, 'base/index.html', context)

def about(request):
    context = {}
    return render(request, 'base/about.html', context)

def product(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'base/product.html', context)

def contact(request):
    context = {}
    return render(request, 'base/contact.html', context)

def cart(request):
    #check if user is authenticated
    if request.user.is_authenticated:
        #get customer
        customer = request.user.customer
        #check for customer's order create one or check for existing
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        #get all orderitems that have order on top as parents
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items':items, 'order':order}
    return render(request, 'base/cart.html', context)

def checkout(request):
    #check if user is authenticated
    if request.user.is_authenticated:
        #get customer
        customer = request.user.customer
        #check for customer's order create one or check for existing
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        #get all orderitems that have order on top as parents
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items':items, 'order':order}
    return render(request, 'base/checkout.html', context)
