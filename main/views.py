from django.shortcuts import render

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user = request.user
        fname = user.first_name
        return render(request, "main/main.html" , {'fname':fname})
    else:
        return render(request, "main/main.html" )
    