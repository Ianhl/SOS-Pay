from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User,Customer
from paystackpay import settings
from django.core.mail import send_mail
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from wallet.models import Wallet
from django.shortcuts import get_object_or_404, render
from main.views import main
from .encryption import decrypt, encrypt



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
        email = request.POST['email']
        pass1 = request.POST['pass1']

        user = authenticate(email=email, password=pass1)

        if user is not None:
            
            # return render(request, "authentication/index.html", {'fname': fname})
            if user.last_login == None:
                login(request, user)
                return redirect('multi')
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
        wallet.pin = encrypt(str(pin2))
        wallet.save()
        return redirect('main')
        
        
       

    return render(request, "authentication/pin.html")

# def signinup(request):
#     status = "remove"
#     return render(request, "authentication/signinup.html", {"status":status})

def multi(request):
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
        
        
        user = request.user
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
        
        customer.is_active = True
        customer.save()
        
        return redirect('pin')  
        
    return render(request, "authentication/multi.html")




# def shop_signup(request):
#     if request.method == "POST":
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']

#         if User.objects.filter(email=email):
#             messages.error(request, "Email already exists. Try other email")
#             return redirect('home')

#         if pass1 != pass2:
#             messages.error(request, "Passwords didn't match")

#         myuser = User.objects.create_shopowner(email=email, password=pass1)
#         myuser.first_name = fname
#         myuser.last_name = lname

#         myuser.save()
#         Wallet.objects.create(
#             user = myuser,
#             balance = 0,
#             pin = 000000,
#             is_shopowner = True,
#         )
        

#         messages.success(request, "Account successfully created.")

#         #Welcome email
#         subject = "Welcome to SOS Pay!"
#         message = "Hello " + myuser.first_name + "!!\n" + "Welcome to SOS Pay\n Thank You for signing up to sell here.\n Your account is currently not verified, hence signin will not be possible. You will be verified within the next 5 days.\n You will recieve an email to activate your account once you are verified. \n If you don't receive this email in the alloted time, kindly send a follow up email. \n\n  Thank you "+fname+ " for choosing SOS Pay!"
#         from_email = 'larteyian@gmail.com'
#         receipient_list = [myuser.email]
#         send_mail(subject, message, from_email, receipient_list, fail_silently=False)



#         return redirect('shop_signin')
    
#     return render(request, "authentication/signinup.html")
