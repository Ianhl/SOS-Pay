from django.shortcuts import redirect, render, get_object_or_404

from authentication.models import User, shop_owner
from vendors.models import Store
from wallet.models import Wallet
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout

# Create your views here.
# def vendor_home(request):
#     if request.user.is_authenticated:
#         user = request.user
#         vendor = get_object_or_404(Store, user = user)
#         shop_owner = get_object_or_404(shop_owner, user=user)
#         shop_name = vendor.shop_name
#         vendor_name = shop_owner.vendor_name
#         return render(request, "vendor/index.html" , {'shop_name':shop_name, 'vendor_name':vendor_name})
#     else:
#         return render(request, "vendor/index.html" )
    

# def vendor_signup(request):
#     if request.method == "POST":
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']
#         shop_name = request.POST['shopname']

#         if User.objects.filter(email=email):
#             messages.error(request, "Email already exists. Try other email")
#             return redirect('vendor_home')

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
        
#         shop_owner.objects.create(
#             user = myuser,
#         )
#         Store.objects.create(
#             user = myuser,
#             vendor_name = shop_name
#         )
        

#         messages.success(request, "Account successfully created.")

#         #Welcome email
#         subject = "Welcome to SOS Pay Vendors!"
#         message = "Hello " +  + "!!\n" + "Welcome to SOS Pay\n Thank You for signing up to sell here.\n Your account is currently not verified, hence signin will not be possible. You will be verified within the next 5 days.\n You will recieve an email to activate your account once you are verified. \n If you don't receive this email in the alloted time, kindly send a follow up email. \n\n  Thank you "+fname+ " for choosing SOS Pay!"
#         from_email = 'larteyian@gmail.com'
#         receipient_list = [myuser.email]
#         send_mail(subject, message, from_email, receipient_list, fail_silently=False)



#         return redirect('vendor_signin')
    
#     return render(request, "vendor/register.html")

# def vendor_signin(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         pass1 = request.POST['pass1']
#         user = authenticate(email=email, password=pass1)

#         # if user is not None:
            
#         #     # return render(request, "authentication/index.html", {'fname': fname})
#         #     # if user.last_login == None:
#         #     #     login(request, user)
#         #     #     return redirect('multi')
#         #     # else:
#         #     #     login(request, user)
#         #     #     return redirect('main')
            
#         # else:
#         #     messages.error(request, "Bad Credentials")
#         #     return redirect('vendor_home')

#     return render(request, "vendor/login.html")


