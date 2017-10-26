# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from ..login_registration.models import User
from .models import Category, Subcategory, Product

def index(request):
    if request.session['logged'] == False:
        return redirect('/')
    if 'cart' not in request.session:
        request.session['cart'] = []
    context = {
        'products': Product.objects.all().order_by('category'),
        'categories': Category.objects.all(),
    }
    return render(request, 'shopping/index.html', context)

def productpage(request, product):
    if request.session['logged'] == False:
        return redirect('/')
    context = {
        'product': Product.objects.get(id=product),
    }
    return render(request, 'shopping/productpage.html', context)

def categorypage(request, category):
    if request.session['logged'] == False:
        return redirect('/')
    context = {
        'category': Category.objects.get(id=category),
        'subcategories': Category.objects.get(id=category).subcategories.all(),
    }
    return render(request, 'shopping/categorypage.html', context)

def subcategorypage(request, category, subcategory):
    if request.session['logged'] == False:
        return redirect('/')
    context = {
        'subcategory': Subcategory.objects.get(id=subcategory),
        'category': Category.objects.get(id=category),
    }
    return render(request, 'shopping/subcategorypage.html', context)

def newproducts(request):
    if request.session['user_id'] != 1:
        return redirect('/store')
    context = {
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all().order_by('category'),
    }
    return render(request, 'shopping/newproducts.html', context)

def create(request):
    if request.session['user_id'] != 1:
        return redirect('/store')
    try:
        Category.objects.get(id=request.POST['category']).subcategories.get(id=request.POST['subcategory'])
        Product.objects.create(name=request.POST['name'], price=request.POST['price'], category=Category.objects.get(id=request.POST['category']))
        Product.objects.last().subcategory.add(Subcategory.objects.get(id=request.POST['subcategory']))
        return redirect('/store')
    except:
        return redirect('/store/newproducts')

def cart(request):
    if request.session['logged'] == False:
        return redirect('/')
    context = {
        'products': [],
        'total': 0.00
    }
    for i in range(0, len(request.session['cart'])):
        context['products'].append(Product.objects.get(id=request.session['cart'][i]))
        context['total'] += float(context['products'][i].price)
    return render(request, 'shopping/cart.html', context)

def addtocart(request, product):
    if request.session['logged'] == False:
        return redirect('/')
    temp = request.session['cart']
    temp.append(product)
    request.session['cart'] = temp
    request.session['cartsize'] = len(request.session['cart'])
    return redirect('/store')

def removefromcart(request, product):
    if request.session['logged'] == False:
        return redirect('/')
    temp = request.session['cart']
    for i in range(0, len(request.session['cart'])):
        # print request.session['cart'][i]
        if request.session['cart'][i] == product:
            request.session['cart'].pop(i)
            break
    request.session['cart'] = temp
    request.session['cartsize'] = len(request.session['cart'])
    return redirect('/store/cart')

def newcategory(request):
    if request.session['logged'] == False:
        return redirect('/')
    Category.objects.create(name=request.POST['name'])
    return redirect('/store/newproducts')
    
def newsubcategory(request):
    if request.session['logged'] == False:
        return redirect('/')
    Subcategory.objects.create(name=request.POST['name'], category=Category.objects.get(id=request.POST['category']))
    return redirect('/store/newproducts')