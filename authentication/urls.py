from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('pin', views.pin, name="pin"),
    path('otp', views.otp_view, name="otp"),
    path('multi/<int:user_id>/', views.multi, name="multi"),
    
    
    # path('signinup', views.signinup, name="signinup"),
]
