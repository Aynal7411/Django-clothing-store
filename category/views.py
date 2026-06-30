from django.shortcuts import render, redirect
from .models import Category
from product.models import Product
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def category_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'products': products,
             }                         
    return render(request, 'category_list.html' , context)
# category/views.py

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Compose the email
        subject = f"Contact from {name}"
        body = f"Message from {name} ({email}):\n\n{message}"

        try:
            send_mail(
                subject,
                body,
                'aynalhaque7411@gmail.com',  # replace with your email
                ['housemilon23@gmail.com'],  # replace with your receiving email
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        
        return redirect('product_list')  # ✅ will work only if 'home' is defined in urls.py

    return render(request, 'contact.html')
