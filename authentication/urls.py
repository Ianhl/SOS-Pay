from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('pin', views.pin, name="pin"),
    path('multi', views.multi, name="multi"),
    
    # path('signinup', views.signinup, name="signinup"),
]
