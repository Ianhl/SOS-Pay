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
from django.shortcuts import get_object_or_404, render
from main.views import main


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
            pin = 000000,
        )

        messages.success(request, "Account successfully created.")


        #Welcome email
        subject = "Welcome to SOS Pay!"
        message = "Hello " + myuser.first_name + "!!\n" + "Welcome to SOS Pay\n Thank You for visiting this site.\n We have sent you a confirmation email. Please confirm your email address to activate your account. \n\n  Thank you "+fname
        from_email = 'larteyian@gmail.com'
        receipient_list = [myuser.email]
        send_mail(subject, message, from_email, receipient_list, fail_silently=False)



        return redirect('signin')
    
    return render(request, "authentication/signinup.html", {"status":status})

def signin(request):
    status = "remove"
    if request.method == "POST":
        email = request.POST['email']
        pass1 = request.POST['pass1']

        user = authenticate(email=email, password=pass1)

        if user is not None:
            
            # return render(request, "authentication/index.html", {'fname': fname})
            if user.last_login == None:
                login(request, user)
                return redirect('pin')
            else:
                login(request, user)
                return redirect('main')
            
        else:
            messages.error(request, "Bad Credentials")
            return redirect('signin')

    return render(request, "authentication/signinup.html", {"status":status})

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('main')

def pin(request):
    if request.method == "POST":
        p1 = request.POST['p1']
        p2 = request.POST['p2']
        p3 = request.POST['p3']
        p4 = request.POST['p4']
        p5 = request.POST['p5']
        p6 = request.POST['p6']
        pin1 = int(str(p1)+str(p2)+str(p3)+str(p4)+str(p5)+str(p6))
        second_p1 = request.POST['2p1']
        second_p2 = request.POST['2p2']
        second_p3 = request.POST['2p3']
        second_p4 = request.POST['2p4']
        second_p5 = request.POST['2p5']
        second_p6 = request.POST['2p6']
        pin2 = int(str(second_p1)+str(second_p2)+str(second_p3)+str(second_p4)+str(second_p5)+str(second_p6))
        
        if pin1 != pin2:
            messages.error(request, "Pins didn't match")
        user = request.user
        wallet = get_object_or_404(Wallet, user = user)
        wallet.pin = pin
        return redirect('main')
        
        
       

    return render(request, "authentication/pin.html")

# def signinup(request):
#     status = "remove"
#     return render(request, "authentication/signinup.html", {"status":status})
