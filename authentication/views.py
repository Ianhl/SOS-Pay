from datetime import datetime
import random
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import pyotp
from .models import User,Customer, shop_owner
from vendors.models import Store
from paystackpay import settings
from django.core.mail import send_mail
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from wallet.models import Wallet
from django.shortcuts import get_object_or_404, render
from main.views import main
from wallet.encryption import decrypt, encrypt
from .utils import send_otp
from django.contrib.auth.decorators import login_required

# wallets are owned by users.

# User = get_user_model

# Create your views here.

# def home(request):
#     return render(request, "authentication/index.html")

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
            return redirect('main')

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
        Customer.objects.create(
            user = myuser,
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
        email = request.POST['email1']
        pass1 = request.POST['pass']

        user = authenticate(email=email, password=pass1)
        user_id = user.id

        if user is not None:
            
            # return render(request, "authentication/index.html", {'fname': fname})
            if user.last_login == None:
                # login(request, user)
                return redirect(f'/login/multi/{user_id}/')
            else:
                # request.session['user_email']= email
                
                # return redirect('otp')
                # send_otp(request)
                email_otp= send_otp(request)
                # email_otp = send_otp(request)
                subject = "Email Verification!"
                message = "Hello " + user.first_name +  "!!\n" + "Welcome to SOS Pay\n Thank You for visiting this site.\n Below is the otp to complete your login. Please type in this otp in the website to login:\n" +email_otp
                from_email = 'larteyian@gmail.com'
                receipient_list = [user.email]
                send_mail(subject, message, from_email, receipient_list, fail_silently=False)
                request.session['email']=user.email
                return redirect('otp')

            
        else:
            messages.error(request, "Bad Credentials")
            return redirect('signin')

    return render(request, "authentication/signinup.html", {"status":status})



def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('main')

def pin(request):
    user = request.user
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
        
        wallet = get_object_or_404(Wallet, user = user)
        wallet.pin = encrypt(str(pin2))
        wallet.save()
        return redirect('main')
    return render(request, "authentication/pin.html")


def otp_view(request):
    if request.method == "POST":
        p1 = request.POST['p1']
        p2 = request.POST['p2']
        p3 = request.POST['p3']
        p4 = request.POST['p4']
        p5 = request.POST['p5']
        p6 = request.POST['p6']
        otp = int(str(p1)+str(p2)+str(p3)+str(p4)+str(p5)+str(p6))
            
        email = request.session.get('email')
        user =  get_object_or_404(User, email=email)
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    print("Success")
                    login(request, user)

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']

                    return redirect('main')
            else:
                messages.error(request, "Invalid otp")
                print("Invalid")
        else: 
            messages.error(request, "OTP expired")
            print("OTP expired")

    

    return render(request, 'authentication/otp2.html')       
       

    

# def signinup(request):
#     status = "remove"
#     return render(request, "authentication/signinup.html", {"status":status})

def multi(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        grad_year = request.POST['grad_year']
        year_group = request.POST['year_group']
        hostel_group = request.POST['hostel_group']
        hostel = request.POST['hostel']
        room_num = request.POST['room_num']
        parent1_first_name = request.POST['parent1_first_name']
        parent1_last_name = request.POST['parent1_last_name']
        parent1_email = request.POST['parent1_email']
        parent2_first_name = request.POST['parent2_first_name']
        parent2_last_name = request.POST['parent2_last_name']
        parent2_email = request.POST['parent2_email']
        
        customer = get_object_or_404(Customer,user=user)
        
        customer.grad_year = grad_year
        customer.year_group = year_group
        customer.hostel_group = hostel_group
        customer.hostel = hostel
        customer.room_num = room_num
        customer.parent1_first_name = parent1_first_name
        customer.parent1_last_name = parent1_last_name
        customer.parent1_email = parent1_email
        customer.parent2_first_name = parent2_first_name
        customer.parent2_last_name = parent2_last_name
        customer.parent2_email = parent2_email
        customer.student_code = customer.generate_student_code()
        
        customer.is_active = True
        customer.save()
        login(request, user)
        
        return redirect('pin')  
        
    return render(request, "authentication/multi.html")




