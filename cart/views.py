from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from product.models import ProductItem

def get_user_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key or request.session.save()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def cart_detail(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()

    context = {'cart': cart}
    return render(request, 'cart_detail.html', context)


def add_to_cart(request, product_item_id):
    product_item = get_object_or_404(ProductItem, id=product_item_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, defaults={})
    else:
        # For anonymous users, you can use session key or create session cart logic
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_item=product_item)

    if not created:
        # If already exists, increase quantity by 1
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')  

def remove_from_cart(request, cart_item_id):
    item = get_object_or_404(CartItem, id=cart_item_id)
    item.delete()
    return redirect('cart_detail')
