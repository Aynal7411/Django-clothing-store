
from django.db import models
from django.utils.text import slugify

from category.models import Category


SIZE_CHOICES = (
    ("XS", "Extra Small"),
    ("S", "Small"),
    ("M", "Medium"),
    ("L", "Large"),
    ("XL", "Extra Large"),
    ("XXL", "Double Extra Large"),
)


def product_image_upload_path(instance, filename):
    category_slug = slugify(instance.category.name)
    return f"products/{category_slug}/{filename}"


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )

    name = models.CharField(
        max_length=200,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        db_index=True,
    )

    brand = models.CharField(
        max_length=100,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    image = models.ImageField(
        upload_to=product_image_upload_path,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    stock = models.PositiveIntegerField(
        default=0,
    )

    available = models.BooleanField(
        default=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    size = models.CharField(
        max_length=5,
        choices=SIZE_CHOICES,
        blank=True,
    )

    color = models.CharField(
        max_length=50,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        self.available = self.stock > 0

        super().save(*args, **kwargs)

    @property
    def final_price(self):
        """
        Returns discounted price if available,
        otherwise original price.
        """
        return self.discount_price or self.price

    @property
    def discount_percent(self):
        """
        Calculates discount percentage.
        """

        if self.discount_price:

            return int(
                (
                    (self.price - self.discount_price)
                    / self.price
                ) * 100
            )

        return 0

    @property
    def in_stock(self):
        return self.stock > 0


class ProductItem(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="items",
    )

    size = models.CharField(
        max_length=5,
        choices=SIZE_CHOICES,
    )

    color = models.CharField(
        max_length=30,
    )

    stock = models.PositiveIntegerField(
        default=0,
    )

    sku = models.CharField(
    max_length=50,
    unique=True,
    blank=True,
    null=True,
)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Optional variant price",
    )

    class Meta:
        ordering = ("size",)
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

    def __str__(self):
        return f"{self.product.name} | {self.size} | {self.color}"

    @property
    def final_price(self):
        """
        Uses variant price if available,
        otherwise product price.
        """
        return self.price or self.product.final_price
