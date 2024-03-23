import json

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=1,
            update_quantity=cd['update'],
        )
        return redirect('cart_details')
    else:
        return redirect('products')


@require_POST
def cart_product_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    body = json.loads(request.body)
    if quantity := body.get('quantity'):
        cart.add(
            product=product,
            quantity=int(quantity),
            update_quantity=True,
        )

        return HttpResponse(status=200)
    return HttpResponse(status=404)


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_details')


def cart_details(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True
                                        })
    return render(
        request,
        'cart_details.html',
        {'cart': cart, 'active': 'Cart'},
    )
