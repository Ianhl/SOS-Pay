from django.urls import path
from . import views

urlpatterns = [
    path('', views.initiate_payment, name="initiate-payment"),
    path('pay/<str:ref>/', views.verify_payment, name="verify-payment"),
    # path('verify/<int:id>', views.verify),
    ]

