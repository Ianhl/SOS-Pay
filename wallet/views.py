from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from authentication.models import Customer
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

def request_funds(request):
    if request.method == "POST":
        user = request.user
        customer = get_object_or_404(Customer,user=user)
        wallet = get_object_or_404(Wallet, user = user)
        wallet_code = wallet.private_code
        subject = "Funds request"
        message = "Hello " + customer.parent1_first_name +  "!!\n" + "Welcome to SOS Pay\n.\n Your ward will like to request some funds. Go to http://127.0.0.1:8000/pay to make the transaction.\n their unique wallet codeis:" +wallet_code
        from_email = 'larteyian@gmail.com'
        receipient_list = [customer.parent1_email]
        send_mail(subject, message, from_email, receipient_list, fail_silently=False)
        return redirect('wallet')
    return render(request, 'base.html')



