from django.contrib import admin
from .models import ProductCategory, Product, Profile
from django.utils.html import format_html
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Main Info", {"fields": ["name", "category", "price", "photo"]}),
    ]
    
    list_display = ["id", "name", "price", "category", "created_at", "updated_at", "image_tag"]
    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.photo.url))
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
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Main Info", {"fields": ["first_name", "last_name", "phone_number", "email","profile_pic", "user", "orders"]})
    ]
    list_display = ["first_name", "last_name", "phone_number", "email", "image_tag", "user", "created_at", "updated_at"]
    list_filter = ["id", "first_name", "last_name", "phone_number", "user", "email"]
    search_fields = ["first_name", "last_name", "phone_number"]
    ordering = ["id"]
    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.profile_pic.url))

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Profile, ProfileAdmin)