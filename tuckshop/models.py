from django.db import models
import uuid

from authentication.models import User
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
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    class Meta:
        ordering = ['product_name']
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    
    def __str__(self):
        return self.product_name

    
class UploadImageModel(models.Model):
    image = models.ImageField(upload_to="images")
    # product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True)
    
    # def __str__(self):
    #     return f"Image for {self.product.name}"

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Order- {str(self.id)}'
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'OrderItem- {str(self.id)}'
    
    def get_total_price(self):
        return self.product.price * self.quantity
    

class Sale(models.Model):
    order = models.OneToOneField(Order, related_name='sale', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale - Order {self.order.id}"

    @property
    def total_quantity(self):
        """Calculate the total quantity of products in this sale."""
        return sum(item.quantity for item in self.order.items.all())

    @property
    def total_price(self):
        """Calculate the total price of this sale."""
        return self.order.get_total_price()


    