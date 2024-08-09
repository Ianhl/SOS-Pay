from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from paystackpay import settings
from django.core.mail import send_mail
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from wallet.models import Wallet

# wallets are owned by users.



# User = get_user_model

# Create your views here.

def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    status = "active"
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(email=email):
            messages.error(request, "Email already exists. Try other email")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match")

        
        

        myuser = User.objects.create_user(email=email, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        Wallet.objects.create(
            user = myuser,
            balance = 0,
            password = pass1,
        )

        messages.success(request, "Account successfully created.")


        #Welcome email
        subject = "Welcome to SOS Pay!"
        message = "Hello" + myuser.first_name + "!! \n" + "Welcome to SOS Pay \n Thank You for visiting this site \n We have sent you a confirmation email. Please confirm your email address to activate your account. \n\n  Thank you "+fname
        from_email = 'hgicpay@gmail.com'
        receipient_list = [myuser.email]
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=receipient_list, fail_silently=True)



        return redirect('signin')
    
    return render(request, "authentication/signinup.html", {"status":status})

def signin(request):
    status = "remove"
    if request.method == "POST":
        email = request.POST['email']
        pass1 = request.POST['pass1']

        user = authenticate(email=email, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            # return render(request, "authentication/index.html", {'fname': fname})
            return redirect('setpin')
        else:
            messages.error(request, "Bad Credentials")
            return redirect('home')

    return render(request, "authentication/signinup.html", {"status":status})

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

# def signinup(request):
#     status = "remove"
#     return render(request, "authentication/signinup.html", {"status":status})
