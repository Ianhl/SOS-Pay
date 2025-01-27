from django.shortcuts import render
import datetime
from django.contrib.auth.decorators import login_required

from authentication.models import Customer

# Create your views here.
current_time = datetime.datetime.now()
def main(request):
    if request.user.is_authenticated:
        user = request.user
        fname = user.first_name
        greeting = greet(current_time.hour)
        return render(request, "main/main.html" , {'fname':fname, 'greeting':greeting})
    else:
        return render(request, "main/main.html" )
    
def greet(time):
    if time in range(1,11):
        greeting = "Good Morning,"
    elif time in range(11,19):
        greeting = "Good Afternoon,"
    else: 
        greeting = "Good Evening,"
    return greeting

@login_required
def customer_detail(request):
    user =request.user
    customer = Customer.objects.get(user=user)
    return render(request, 'authentication/profile.html', {'customer': customer})