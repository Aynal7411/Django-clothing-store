from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Product
from category.models import Category


def product_list(request):
    products = Product.objects.select_related("category").filter(
        available=True
    )

    categories = Category.objects.all()

    category_slug = request.GET.get("category")
    search = request.GET.get("search")

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(brand__icontains=search)
        )

    context = {
        "products": products,
        "categories": categories,
        "selected_category": category_slug,
        "search": search,
    }

    return render(request, "product_list.html", context)


def product_detail(request, slug):

    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug,
        available=True,
    )

    related_products = Product.objects.filter(
        category=product.category,
        available=True,
    ).exclude(
        id=product.id
    )[:4]

    context = {
        "product": product,
        "related_products": related_products,
    }

    return render(request, "product_detail.html", context)