from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}
    return render(request, 'base/index.html', context)

def about(request):
    context = {}
    return render(request, 'base/about.html', context)

def product(request):
    context = {}
    return render(request, 'base/product.html', context)

def contact(request):
    context = {}
    return render(request, 'base/contact.html', context)

def cart(request):
    context = {}
    return render(request, 'base/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'base/checkout.html', context)
