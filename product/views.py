# product/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product,ProductItem
from category.models import Category
def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products, 'categories': categories})

def product_detail(request, slug):
     product = get_object_or_404(Product, slug=slug)
     product_items = ProductItem.objects.filter(product=product)
    
     return render(request, 'product_detail.html', {'product': product, 'product_items': product_items})
