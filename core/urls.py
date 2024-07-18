from django.urls import path
from . import views

urlpatterns = [
    path('', views.initiate_payment, name="initiate-payment"),
    path('<str:ref>/', views.verify_payment, name="verify-payment"),
    # path('verify/<int:id>', views.verify),
    ]

