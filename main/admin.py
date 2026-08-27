from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'is_active', 'views', 'get_miniature')
    list_display_links = ('id', 'name')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('views', 'created_at')

    def get_miniature(self, item):
        if item.image:
            return format_html(
                '<img src="{}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                item.image.url
            )
        return format_html('<span style="color: #999; font-style: italic;">Без фото</span>')

    get_miniature.short_description = "Мініатюра"