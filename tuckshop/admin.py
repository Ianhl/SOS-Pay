from django.contrib import admin
from .models import Product, UploadImageModel, Order, OrderItem
# Register your models here.

admin.site.register(Product) 
admin.site.register(UploadImageModel) 
admin.site.register(Order) 
admin.site.register(OrderItem) 