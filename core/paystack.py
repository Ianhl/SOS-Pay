from django.conf import settings
import requests
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse

class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = 'https://api.paystack.co'

    def verify_payment(self, ref, *args, **kwargs):
        path = f'/transaction/verify/{ref}'

        headers = {
            "Authorization": f"Bearer{self.PAYSTACK_SECRET_KEY}",
            'Content-Type': 'application/json',
        }
        url = self.base_url + path
        response = requests.get(url)

        if response.status_code == 200:
            x=True
            response_data = response.json()
            return response_data["status"], response_data["data"]
        else:
            response_data = response.json()
            return response_data["status"], response_data["message"] ######
        
    