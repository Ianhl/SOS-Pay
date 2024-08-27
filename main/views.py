from django.shortcuts import render
import datetime

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
    elif time in range(12,6):
        greeting = "Good Afternoon,"
    else: 
        greeting = "Good Evening,"
    return greeting
