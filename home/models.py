from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import os


#define path for each user profile
#will create a folder for each user profile picture
def user_profile_pic_path(instance, filename):
    user_id = str(instance.user.id)
    upload_path = os.path.join('users', 'images', 'user', user_id, filename)
    return upload_path

#define user default pic path if not set
def user_profile_pic_default():
    return "users/images/default/default_profile_pic.png"


# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=48)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)
    
    #Meta class db_table attribute used to override 
    #django default naming scheme for database table name
    class Meta:
        db_table = "ProductCategories"
        verbose_name_plural = "Product Categories"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=48)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)
    photo = models.ImageField(upload_to='images')
    class Meta:
        db_table = "Products"

    def __str__(self):
        return self.name



class Order(models.Model):
    order_date = models.DateTimeField("Order Date", auto_now_add=True)
    special_instruction = models.CharField("Special Instruction", max_length=256)
    products = models.ManyToManyField(Product)
    updated_at = models.DateTimeField("Created at", auto_now=True)
    class Meta:
        db_table = "Orders"

class Profile(models.Model):
    first_name = models.CharField("First Name",max_length=128)
    last_name = models.CharField("Last Name", max_length=64)
    phone_number = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order, blank=True)
    class Meta:
        db_table = "Profile"

    def __str___(self):
        return self.first_name + " " + self.last_name
