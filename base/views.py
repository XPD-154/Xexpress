from django.shortcuts import render
from .models import *                   #import all models into view
from .utils import *                    #import all functions into view
from django.http import JsonResponse
import requests
import json
import datetime

#Create your views here.

def index(request):
    products = Product.objects.all().order_by('id')[:3]

    #check if user is authenticated
    if request.user.is_authenticated:
        #get cart item total
        cartData = cartItemsCheck(request)
    else:
        cookieData = cookieCart(request)
        cartData = cookieData['cartItems']

    context = {'products':products, 'cartItems':cartData}
    return render(request, 'base/index.html', context)

def about(request):
    context = {}
    return render(request, 'base/about.html', context)

def product(request):
    products = Product.objects.all()

    #check if user is authenticated
    if request.user.is_authenticated:

        data = cartInfo(request)
        items = data['items']
        order = data['order']

        #get cart item total
        cartItemsNumber = order.get_cart_items
        cartData = cartItems(request, cartItemsNumber)

    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartData = cookieData['cartItems']

    context = {'products':products, 'cartItems':cartData}
    return render(request, 'base/product.html', context)

def contact(request):
    context = {}
    return render(request, 'base/contact.html', context)

def cart(request):
    #check if user is authenticated
    if request.user.is_authenticated:

        data = cartInfo(request)
        items = data['items']
        order = data['order']

        #get cart item total
        cartItemsNumber = order.get_cart_items
        cartData = cartItems(request, cartItemsNumber)

    #user thats not logged in
    else:
        cookieData = cookieCart(request)
        cartData = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']

    context = {'items':items, 'order':order, 'cartItems':cartData}
    return render(request, 'base/cart.html', context)

def checkout(request):
    #check if user is authenticated
    if request.user.is_authenticated:

        data = cartInfo(request)
        items = data['items']
        order = data['order']

        #get cart item total
        cartData = cartItemsCheck(request)
    else:
        cookieData = cookieCart(request)
        cartData = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']

    context = {'items':items, 'order':order, 'cartItems':cartData}
    return render(request, 'base/checkout.html', context)

def updateItem(request):

    #load items from javascript API and make items available
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    #get signed in customer, the product, order and order item
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    #add or remove from orderitem quantity
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    #save after changes
    orderItem.save()

    #if orderitem quantity is zero, delete
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)

def processOrder(request):
    #print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode']
            )
    else:
        print('User is not logged in..')

    return JsonResponse('payment complete', safe=False)
