from django.shortcuts import get_object_or_404, render

from wallet.models import Wallet

# Create your views here.
def wallet(request):
    if request.user.is_authenticated:
        user = request.user
        fname = user.first_name
        wallet = get_object_or_404(Wallet, user = user)
        balance = wallet.balance
        return render(request, "main/wallet.html" , {'fname':fname, 'balance':balance})
    else: 
        return render(request, "main/wallet.html")


