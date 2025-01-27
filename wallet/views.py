from django.shortcuts import get_object_or_404, render, redirect

from wallet.models import Wallet, Transaction
from main.views import main
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def wallet(request):
    if request.user.is_authenticated:
        user = request.user
        fname = user.first_name
        wallet = get_object_or_404(Wallet, user = user)
        balance = wallet.balance
        private_code = wallet.private_code
        transactions = wallet.transaction_set.order_by('-created_at')
        paginator = Paginator(transactions, 5)  # 5 transactions per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "main/wallet.html" , {'fname':fname, 'balance':balance, 'private_code':private_code, 'wallet':wallet, 'page_obj':page_obj})
    else: 
        return redirect('main')


