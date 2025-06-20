from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.wallet, name="wallet"),
    path('request', views.request_funds, name="wallet"),
]
    