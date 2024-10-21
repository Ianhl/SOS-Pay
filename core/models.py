from django.db import models
import secrets

from django.http import JsonResponse
from .paystack import PayStack
from pypaystack import Transaction
from django.conf import settings

# Create your models here.
class Payment(models.Model):
    amount = models.PositiveBigIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField(help_text="Input your email")
    receipient_email = models.EmailField(help_text="")
    receipient_code = models.CharField(max_length=20, help_text="Please input the receipient/student's unique wallet code")
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)
    
    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.amount *100

    def verify_payment(self):
        transaction = Transaction(authorization_key= settings.PAYSTACK_SECRET_KEY)
        response = transaction.verify(self.ref)
        data = JsonResponse(response, safe=False)
        status = response[1]
        result = response[3]
        if status:
            if result['amount']/100 == self.amount:
                self.verified = True 
            self.save()
        if self.verified:
            return True
        else:
            return False
    # def verify(request, id):
#     transaction = Transaction(authorization_key= settings.PAYSTACK_SECRET_KEY)
#     response = transaction.verify(id)
#     data = JsonResponse(response, safe=False)
#     return data