from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.tuckshop_main, name="tuckshop_main"),
    
]
