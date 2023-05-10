from django.shortcuts import render, redirect
from .models import *                   #import all models into view
from .utils import *                    #import all functions into view
from django.http import JsonResponse
import requests
import json
import datetime
import decimal
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib import messages

#Create your views here.

#method to handle login request
def login_pg(request):

    if request.method == 'POST':
        username = request.POST['name'].lower()
        password = request.POST['password'].lower()

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, 'Logged in successfully!!!')
            return redirect('index')
        else:
            messages.info(request, 'username or password incorrect!!!')
            return redirect('login_pg')
    else:
        return render(request, "login.html")

#method to handle logout request
def logout(request):
    django_logout(request)
    return redirect('index')

#method to handle sign up request
def sign_up_pg(request):

    if request.method == 'POST':

        email = request.POST['email'].lower()
        username = request.POST['name'].lower()
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:

            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():

                #print('username or email already taken')
                messages.info(request, 'username or email already taken')
                return redirect('sign_up_pg')

            else:

                user = User.objects.create_user(email=email, password=password1, username=username)
                user.save();

                user_new = User.objects.get(email=email)

                customer, created = Customer.objects.get_or_create(user=user_new, name=username, email=email)

                messages.info(request, 'user created')
                #print('user created')

                new_user = authenticate(username=username, password=password1)
                login(request, new_user)

                return redirect('index')
        else:

            #print('check password!!')
            messages.info(request, 'check password!!')
            return redirect('sign_up_pg')

    else:

        return render(request, "sign_up.html")

#method to handle homepage display
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

#method to handle about page display
def about(request):
    context = {}
    return render(request, 'base/about.html', context)

#method to handle product display on a page
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

#method to handle display on contact us page
def contact(request):
    context = {}
    return render(request, 'base/contact.html', context)

#method to handle cart information
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

#method to handle checkout
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

#method to handle update of items in cart
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

#method to handle processing of ecommerce request
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
