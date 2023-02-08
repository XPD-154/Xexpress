from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}
    return render(request, 'base/index.html', context)

def cart(request):
    context = {}
    return render(request, 'base/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'base/checkout.html', context)
