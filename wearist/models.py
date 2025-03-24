from django.db import models

# Create your models here.

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")  
    colour = models.CharField(max_length=50)
    imageurl = models.CharField(max_length=300)
    size = models.CharField(max_length=2)
    instock = models.BooleanField(default=True)
    material = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(max_length=800, null= True, blank=True)

    def __str__(self):
        return self.name

