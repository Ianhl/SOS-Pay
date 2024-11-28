from django.shortcuts import get_object_or_404, render

from wallet.models import Wallet

# Create your views here.
def wallet(request):
    if request.user.is_authenticated:
        user = request.user
        fname = user.first_name
        wallet = get_object_or_404(Wallet, user = user)
        balance = wallet.balance
        private_code = wallet.private_code
        return render(request, "main/wallet.html" , {'fname':fname, 'balance':balance, 'private_code':private_code})
    else: 
        return render(request, "main/wallet.html")


