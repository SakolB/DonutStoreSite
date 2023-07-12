from django.contrib import admin
from .models import ProductCategory, Product, Customer
# Register your models here.
class ProductCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Main Info", {"fields": ["name"]}),
        ("Detail", {"fields": ["created_at", "updated_at"]}),
    ]

    list_display = ["name", "created_at", "updated_at"]
    list_filter = ["name", "created_at", "updated_at"]

admin.site.register(ProductCategory, ProductCategoryAdmin)