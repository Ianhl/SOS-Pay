from django.shortcuts import get_object_or_404, render

from wallet.models import Wallet

# Create your views here.
def home(request):
    user = request.user
    fname = user.first_name
    wallet = get_object_or_404(Wallet, user = user)
    balance = wallet.balance
    return render(request, "main/wallet.html" , {'fname':fname, 'balance':balance})