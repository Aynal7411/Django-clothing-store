from django.db import models
from django.utils.text import slugify
from category.models import Category

# Size options for clothing
SIZE_CHOICES = [
    ('XS', 'Extra Small'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
    ('XXL', 'Double Extra Large'),
]

def product_image_upload_path(instance, filename):
    return f'products/{instance.category.name}/{filename}'

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to=product_image_upload_path)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, blank=True)
    color = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

        
class ProductItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    size = models.CharField(max_length=10, choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')])
    color = models.CharField(max_length=20)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.color}"
