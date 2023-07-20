from django.contrib import admin
from .models import ProductCategory, Product, Customer
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Main Info", {"fields": ["name", "category", "price", "photo"]}),
    ]
    
    list_display = ["id", "name", "price", "category", "created_at", "updated_at", "photo"]
    list_filter = ["id", "name", "price", "category", "created_at", "updated_at"]
    search_fields = ["name", "category__name"]
    ordering = ["id"]
class ProductCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Main Info", {"fields": ["name"]}),
    ]
    ordering = ["id"]
    list_display = ["id", "name", "created_at", "updated_at"]
    list_filter = ["id", "name", "created_at", "updated_at"]

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)