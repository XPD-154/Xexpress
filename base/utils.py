from django.shortcuts import render
from .models import *                   #import all models into view
from django.http import JsonResponse
import requests
import json
import datetime

#create functions and methods here

'''check and update cart item total based on items added'''

def cartItems(request, number):
    request.session['cartItems'] = number
    return request.session['cartItems']

def cartItemsCheck(request):
    if 'cartItems' in request.session:
        cartData = request.session['cartItems']
    else:
        cartData = cartItems(request, 0)

    return cartData

'''end of check and update cart item total based on items added'''

'''function for shopping associated with user thats not logged in'''

def cookieCart(request):
    #get cookies and convert to py dictionary
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart=', cart)

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}

    #get cart item total
    cartItemsNumber = order['get_cart_items']

    #looping through cookies cart
    for i in cart:
        #if product doesnt exist anymore, just escape it
        try:
            cartItemsNumber += cart[i]['quantity']

            #get product from database
            product = Product.objects.get(id=i)
            #get price from database and multiply with cart quantity to equal total
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            #create similar dictionary for items and append to the real item
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity':cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)

            #shipping information
            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    #set cartData to cartItemsNumber
    cartData = cartItemsNumber

    return {'items':items, 'order':order, 'cartItems':cartData}

'''end of function for shopping associated with user thats not logged in'''

'''function for handling shopping cart, for logged in user'''

def cartInfo(request):

    #get customer
    customer = request.user.customer
    #check for customer's order create one or check for existing
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #get all orderitems that have order on top as parents
    items = order.orderitem_set.all()

    return {'items':items, 'order':order}

'''end of function for handling shopping cart, for logged in user'''
