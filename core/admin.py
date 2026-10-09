from django.contrib import admin
from .models import Category, Dish, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)
    ordering = ("order", "name")


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available", "order")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")
    list_editable = ("price", "is_available", "order")
    ordering = ("order", "name")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "created_at", "is_approved")
    list_filter = ("is_approved", "rating", "created_at")
    search_fields = ("name", "text")
    list_editable = ("is_approved",)
    readonly_fields = ("created_at",)