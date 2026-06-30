from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True)

    description = models.TextField(
        blank=True,
        null=True
    )

    icon = models.ImageField(
        upload_to="category_icons/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name