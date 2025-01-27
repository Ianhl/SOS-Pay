from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Sale

# @receiver(post_save, sender=Order)
# def create_sale(sender, instance, created, **kwargs):
#     if created:
#         Sale.objects.create(order=instance)