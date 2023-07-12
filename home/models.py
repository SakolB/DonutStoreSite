from django.db import models

# Create your models here.
class ProductCategories(models.Model):
    name = models.CharField(max_length=48)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)
    
    #Meta class db_table attribute used to override 
    #django default naming scheme for database table name
    class Meta:
        db_table = "ProductCategories"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)
    name = models.CharField(max_length=48)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)
    class Meta:
        db_table="Products"
        
    def __str__(self):
        return self.name
    