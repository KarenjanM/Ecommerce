import json
import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.views import LoginView, reverse_lazy
from .models import *

def store(request):
    products = Product.objects.all()
    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0}
    cart_items = order['get_cart_items']
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        if 'items' in request.session and 'order' in request.session:
            items = request.session['items']
            order = request.session['order']
            cart_items = order['get_cart_items']
        else:
            if 'items' in request.session and 'order' in request.session:
                items = request.session['items']
                order = request.session['order']
                cart_items = order['get_cart_items']
    context = {
        'products': products,
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'base/store.html', context)


def cart(request):
    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0}
    cart_items = order['get_cart_items']
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        if 'items' in request.session and 'order' in request.session:
            items = request.session['items']
            order = request.session['order']
            cart_items = order['get_cart_items']
    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items

    }
    return render(request, 'base/cart.html', context)


def checkout(request):
    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0}
    cart_items = order['get_cart_items']
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        if 'items' in request.session and 'order' in request.session:
            items = request.session['items']
            order = request.session['order']
            cart_items = order['get_cart_items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items
    }
    return render(request, 'base/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    print('product_id', product_id, 'action', action)

    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_item, created = OrderItem.objects.get_or_create(product=product, order=order)

        if action == 'add':
            order_item.quantity = (order_item.quantity + 1)
        elif action == 'remove':
            order_item.quantity = (order_item.quantity - 1)

        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()
    else:
        product = Product.objects.get(id=product_id)
        if 'items' not in request.session:
            items = request.session['items'] = {}
        else:
            items = request.session['items']
        if 'order' not in request.session:
            order = request.session['order'] = {'get_cart_total': 0, 'get_cart_items': 0}
        else:
            order = request.session['order']
        if product_id not in request.session['items']:
            items[product_id] = {'quantity': 0, 'price': product.float_price, 'image': product.image_url,
                                                    'name': product.name, 'total_price': 0}
        if action == 'add':
            items[product_id]['quantity'] += 1
            order['get_cart_total'] += request.session['items'][product_id]['price']
            order['get_cart_items'] += 1
            items[product_id]['total_price'] += request.session['items'][product_id]['price']
            request.session.modified = True
        elif action == 'remove':
            order['get_cart_total'] -= items[product_id]['price']
            order['get_cart_items'] -= 1
            items[product_id]['quantity'] -= 1
            items[product_id]['total_price'] -= request.session['items'][product_id]['price']
            request.session.modified = True
            if items[product_id]['quantity'] == 0:
                del items[product_id]
    return JsonResponse('item was added', safe=False)


def process_order(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping_info']['address'],
                city=data['shipping_info']['city'],
                state=data['shipping_info']['state'],
                zipcode=data['shipping_info']['zipcode']
            )
    else:
        total = float(data['form']['total'])
        if total == request.session['order']['get_cart_total']:
            ShippingAddress.objects.create(
                customer=None,
                order=None,
                address=data['shipping_info']['address'],
                city=data['shipping_info']['city'],
                state=data['shipping_info']['state'],
                zipcode=data['shipping_info']['zipcode']
            )
        request.session.flush()
    print('Data', data)
    return JsonResponse('Payment is complete', status=200, safe=False)


def delete_session(request):
    request.session.flush()
    return JsonResponse('session is deleted', safe=False)


def product_view(request, product_id):
    product = Product.objects.get(id=int(product_id))
    order = {'get_cart_items': 0, 'get_cart_total': 0}
    cart_items = order['get_cart_items']
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        if 'order' in request.session:
            order = request.session['order']
            cart_items = order['get_cart_items']

    context = {
        'order': order,
        'cart_items': cart_items,
        'product': product,
    }

    return render(request, 'base/product_view.html', context=context)
