from django.conf import settings
import requests
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from pypaystack import Transaction

class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = 'https://api.paystack.co'

    def verify(ref):
        transaction = Transaction(authorization_key= settings.PAYSTACK_SECRET_KEY)
        response = transaction.verify(ref)
        data = JsonResponse(response, safe=False)
        status = response[1]
        result = response[3]
        return status, result