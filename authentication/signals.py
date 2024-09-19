# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import User, finance_team, shop_owner, customer

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.is_financeadmin:
#             finance_team.objects.create(user=instance)
#         elif instance.is_staff:
#             shop_owner.objects.create(user=instance)
#         else:
#             customer.objects.create(user=instance)