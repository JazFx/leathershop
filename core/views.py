from django.shortcuts import render
from .forms import SignUp
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from .models import Cart, Product, OrderItem
from .models import Order
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db import transaction

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user)
    latest_order = Order.objects.filter(user=request.user).last()

    order_item_images = []
    for order in orders:
        for item in order.orderitem_set.all():
            order_item_images.append(item.product.image)

    return render(request, 'profile.html',
                  {'orders': orders, 'latest_order': latest_order, 'order_item_images': order_item_images})

@login_required
def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = 0

        for item in cart_items:
            item.total_price = item.quantity * item.product.price
            total_price += item.total_price

        return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
    else:
        return redirect('login')

@transaction.atomic
def submit_order(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        total_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
        order = Order.objects.create(user=user, total=total_price, address='', payment_method='cash_on_delivery', comment='')
        for cart_item in cart_items:
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
        cart_items.delete()
        messages.success(request, 'Заказ успешно оформлен.')
        return redirect('profile')
    return render(request, 'checkout.html')

@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item = Cart.objects.get(user=request.user, product=product)
    cart_item.delete()
    return HttpResponseRedirect(reverse('cart'))

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart')
    else:
        return redirect('login')

@login_required
def update_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def profile_redirect(request):
    return redirect('home')

def reg(req):
    if req.POST:
        f=SignUp(req.POST)
        if f.is_valid():
            f.save()
            k1 = f.cleaned_data.get('username')
            k2 = f.cleaned_data.get('password1')
            k3 = f.cleaned_data.get('email')
            k4 = f.cleaned_data.get('first_name')
            k5 = f.cleaned_data.get('last_name')

            user = authenticate(username = k1, password = k2)
            newuser = User.objects.get(username=k1)
            newuser.email = k3
            newuser.first_name = k4
            newuser.last_name = k5
            newuser.save()
            login(req,newuser)
            return redirect('home')
    else:
        f=SignUp()
    data = {'forma':f}
    return render(req, 'registration/registration.html', data)