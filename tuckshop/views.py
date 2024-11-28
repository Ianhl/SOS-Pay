from django.shortcuts import render
from .decorator import user_is_tuckshop_owner
# Create your views here.

@user_is_tuckshop_owner
def tuckshop_main(request):
    return render(request, "tuckshop/index.html")