from django.db import models

# Create your models here.
from authentication.models import User

class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    # Add more vendor-related fields here

class Product(models.Model):
    vendor = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to="images/")