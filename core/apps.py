from django.apps import AppConfig
from paystackapi.paystack import Paystack
from django.conf import settings


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

Paystack.secret_key = settings.PAYSTACK_SECRET_KEY
Paystack.public_key = settings.PAYSTACK_PUBLIC_KEY