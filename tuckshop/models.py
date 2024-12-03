from django.db import models
import uuid
# Create your models here.

class Product(models.Model):
    product_choices = [
        ("Drink", "Drink"),
        ("Chips", "Chips"),
        ("Candy", "Candy"),
        ("Cookies", "Cookies"),
    ]
    product_name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images')
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    product_category = models.CharField(max_length=255, default='', choices=product_choices)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    
    
    
    def _str_(self):
        return self.product_name
    
    
    
class UploadImageModel(models.Model):
    image = models.ImageField(upload_to="images")
    # product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True)
    
    # def __str__(self):
    #     return f"Image for {self.product.name}"