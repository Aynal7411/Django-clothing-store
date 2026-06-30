from django.contrib import admin
from django.utils.html import format_html

from .models import Product, ProductItem


class ProductItemInline(admin.TabularInline):
    model = ProductItem
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "name",
        "category",
        "brand",
        "price",
        "discount_price",
        "final_price_display",
        "stock",
        "stock_status",
        "available",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "category",
        "brand",
        "available",
        "is_featured",
        "created_at",
    )

    search_fields = (
        "name",
        "brand",
        "slug",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20

    prepopulated_fields = {
        "slug": ("name",)
    }

    readonly_fields = (
        "created_at",
        "updated_at",
        "image_preview",
    )

    inlines = [
        ProductItemInline,
    ]

    fieldsets = (

        (
            "Basic Information",
            {
                "fields": (
                    "category",
                    "name",
                    "slug",
                    "brand",
                    "description",
                )
            },
        ),

        (
            "Pricing",
            {
                "fields": (
                    "price",
                    "discount_price",
                )
            },
        ),

        (
            "Inventory",
            {
                "fields": (
                    "stock",
                    "available",
                    "is_featured",
                    "size",
                    "color",
                )
            },
        ),

        (
            "Product Image",
            {
                "fields": (
                    "image",
                    "image_preview",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),

    )

    @admin.display(description="Image")
    def image_preview(self, obj):

        if obj.image:
            return format_html(
                '<img src="{}" width="70" height="70" style="border-radius:8px;object-fit:cover;" />',
                obj.image.url,
            )

        return "-"

    @admin.display(description="Final Price")
    def final_price_display(self, obj):
        return obj.final_price

    @admin.display(description="Stock Status")
    def stock_status(self, obj):

        if obj.stock > 10:
            color = "green"
            text = "In Stock"

        elif obj.stock > 0:
            color = "orange"
            text = "Low Stock"

        else:
            color = "red"
            text = "Out of Stock"

        return format_html(
            '<strong style="color:{};">{}</strong>',
            color,
            text,
        )


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "sku",
        "size",
        "color",
        "stock",
        "final_price",
    )

    search_fields = (
        "sku",
        "product__name",
    )

    list_filter = (
        "size",
        "color",
    )

    ordering = (
        "product",
    )

    list_per_page = 25