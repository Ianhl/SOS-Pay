from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse

from authentication.models import User
from . import forms
from django.contrib import messages
from django.conf import settings
from .models import Payment
from pypaystack import Transaction, Customer, Plan
from wallet.models import Wallet
from main.views import main

# Create your views here.

def initiate_payment(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        payment_form = forms.PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()
            email = payment.receipient_email
            wallet_code = payment.receipient_code
            user = get_object_or_404(User, email=email)
            user_fname = user.first_name
            user_lname = user.last_name
            wallet = get_object_or_404(Wallet, user = user)
            if wallet.private_code == wallet_code:
                return render(request, 'make_payment.html', {'fname':user_fname, 'lname':user_lname, 'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
            else:
                messages.error(request, "Email doesn't match code.")
    else:
        payment_form = forms.PaymentForm()

    
    return render(request, 'initiate_payment.html', {'payment_form': payment_form})


def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified == True:
        # user = request.user
        # cwallet = Wallet(user=user)
        # wallet_id = cwallet.id
        code = payment.receipient_code
        wallet = get_object_or_404(Wallet, private_code = code)
        Wallet.deposit(wallet,payment.amount)
        messages.success(request, "Verification Successful")
    else: 
       messages.error(request, "Verification Bad")
    return redirect('main')


# def verify(request, id):
#     transaction = Transaction(authorization_key= settings.PAYSTACK_SECRET_KEY)
#     response = transaction.verify(id)
#     data = JsonResponse(response, safe=False)
#     return data