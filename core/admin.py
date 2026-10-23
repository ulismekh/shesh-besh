
from django.contrib import admin
from .models import Category, Dish, Review


# Общий стиль и русские названия админ-панели
admin.site.site_header = "Shesh-Besh — управление чайханой"
admin.site.site_title = "Shesh-Besh"
admin.site.index_title = "Панель управления"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)
    list_editable = ("order",)
    ordering = ("order", "name")
    list_per_page = 25

    class Meta:
        verbose_name = "Категория меню"
        verbose_name_plural = "Категории меню"


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "half_price",
        "is_available",
        "order",
    )
    list_display_links = ("name",)
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")
    list_editable = ("price", "half_price", "is_available", "order")
    ordering = ("order", "name")
    list_per_page = 30
    list_select_related = ("category",)

    fieldsets = (
        ("Основная информация", {
            "fields": ("name", "category", "description", "image"),
        }),
        ("Цены в сумах", {
            "fields": ("price", "half_price"),
            "description": (
                "Укажите цену полной порции. "
                "Цену полпорции оставьте пустой, если она не продаётся."
            ),
        }),
        ("Отображение в меню", {
            "fields": ("is_available", "order"),
        }),
    )




@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "created_at", "is_approved")
    list_filter = ("is_approved", "rating", "created_at")
    search_fields = ("name", "text")
    list_editable = ("is_approved",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    list_per_page = 30
