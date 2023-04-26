from django.shortcuts import render
from .models import *                   #import all models into view
from .utils import *                    #import all functions into view
from django.http import JsonResponse
import requests
import json
import datetime
import decimal

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

        #call function to handle request for logged in user
        data = cartInfo(request)
        items = data['items']
        order = data['order']

        #get cart item total
        cartItemsNumber = order.get_cart_items
        cartData = cartItems(request, cartItemsNumber)

    else:
        #call function to handle request for anonymous user
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

        #call function to handle request for logged in user
        data = cartInfo(request)
        items = data['items']
        order = data['order']

        #get cart item total
        cartItemsNumber = order.get_cart_items
        cartData = cartItems(request, cartItemsNumber)

    #user thats not logged in
    else:
        #call function to handle request for anonymous user
        cookieData = cookieCart(request)
        cartData = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']

    context = {'items':items, 'order':order, 'cartItems':cartData}
    return render(request, 'base/cart.html', context)

def checkout(request):
    #check if user is authenticated
    if request.user.is_authenticated:

        #call function to handle request for logged in user
        data = cartInfo(request)
        items = data['items']
        order = data['order']

        #get cart item total
        cartData = cartItemsCheck(request)
    else:
        #call function to handle request for anonymous user
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
    #get date for the processing of transaction
    transaction_id = datetime.datetime.now().timestamp()

    #load items from javascript API and make items available
    data = json.loads(request.body)

    #authenticated user
    if request.user.is_authenticated:

        #get information associated with the user
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    #anonymous user
    else:
        print('User is not logged in..')

        print('COOKIES:', request.COOKIES)

        #get user name and email from form
        name = data['form']['name']
        email = data['form']['email']

        #call function for handling cart for anonymous user to get items
        cookieData = cookieCart(request)
        items = cookieData['items']

        #create anonymous customer in database or retrieve based on email
        customer, created = Customer.objects.get_or_create(
            email=email
        )

        #save customer name and save
        customer.name = name
        customer.save()

        #create order for customer in database
        order = Order.objects.create(
            customer = customer,
            complete = False,
        )

        #loop through items in cart and create each order item
        for item in items:
            product = Product.objects.get(id=item['product']['id'])

            orderItem = OrderItem.objects.create(
                product = product,
                order = order,
                quantity = item['quantity']
            )

    #get total from javascript API data
    total = decimal.Decimal(data['form']['total'])
    order.transaction_id = transaction_id

    #compare 'total' from javascript API to 'total' from function in order model, and save
    if total == order.get_cart_total:
        order.complete = True
        order.save()


    #if shipping is true, create shipping information
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
        )

    return JsonResponse('payment complete', safe=False)
