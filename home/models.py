from django.db import models
from django.core.validators import RegexValidator
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
    class Meta:
        db_table = "Products"

    def __str__(self):
        return self.name

class Customer(models.Model):
    phone_regex = RegexValidator(
        regex = r'^\+?1?\d{9, 15}$',
        message = "Phone number must be in the correct U.S number format"
    )
    first_name = models.CharField("First Name",max_length=128)
    last_name = models.CharField("Last Name", max_length=64)
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Customers"

    def __str___(self):
        return self.firstname + " " + self.last_name


class Order(models.Model):
    order_date = models.DateTimeField("Order Date")
    special_instruction = models.CharField("Special Instruction", max_length=256)
    products = models.ManyToManyField(Product)