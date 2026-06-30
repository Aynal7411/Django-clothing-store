from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Cart, CartItem
from product.models import ProductItem


def get_user_cart(request):
    """
    Return current user's cart.
    If user is anonymous, use session cart.
    """

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user
        )
    else:
        if not request.session.session_key:
            request.session.create()

        cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key
        )

    return cart


def cart_detail(request):

    cart = get_user_cart(request)
    items = cart.items.select_related(
        "product_item",
        "product_item__product"
    )
    context = {
          "cart": cart,
        "items": items,
    }

    return render(
        request,
        "cart_detail.html",
        context,
    )


def add_to_cart(request, product_item_id):

    product_item = get_object_or_404(
        ProductItem,
        id=product_item_id
    )

    cart = get_user_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_item=product_item,
    )

    if not created:

        if cart_item.quantity < product_item.stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(
                request,
                "No more stock available."
            )

    return redirect("cart_detail")


def remove_from_cart(request, cart_item_id):

    cart = get_user_cart(request)

    item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart=cart,
    )

    item.delete()

    messages.success(
        request,
        "Item removed from cart."
    )

    return redirect("cart_detail")


def update_cart_item(request, cart_item_id):

    cart = get_user_cart(request)

    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart=cart,
    )

    if request.method == "POST":

        quantity = request.POST.get("quantity")

        try:
            quantity = int(quantity)

            if quantity <= 0:

                cart_item.delete()

                messages.success(
                    request,
                    "Item removed from cart."
                )

            elif quantity > cart_item.product_item.stock:

                messages.error(
                    request,
                    "Requested quantity exceeds stock."
                )

            else:

                cart_item.quantity = quantity
                cart_item.save()

                messages.success(
                    request,
                    "Cart updated successfully."
                )

        except (TypeError, ValueError):

            messages.error(
                request,
                "Invalid quantity."
            )

    return redirect("cart_detail")