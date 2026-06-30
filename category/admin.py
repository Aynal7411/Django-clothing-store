from django.contrib import admin
from django.utils.html import format_html

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "icon_preview",
        "name",
        "slug",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
        "slug",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    readonly_fields = (
        "created_at",
        "updated_at",
        "icon_preview",
    )

    list_per_page = 15

    fieldsets = (

        (
            "Category Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                )
            },
        ),

        (
            "Category Image",
            {
                "fields": (
                    "icon",
                    "icon_preview",
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

    def icon_preview(self, obj):

        if obj.icon:

            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:8px;" />',
                obj.icon.url
            )

        return "No Image"

    icon_preview.short_description = "Icon"