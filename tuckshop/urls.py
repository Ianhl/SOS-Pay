from django.contrib import admin
from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.tuckshop_main, name="tuckshop_main"),
    path('media_upload', ImgUploadAPIview.as_view(), name="media_upload"),
    path('register', views.tuckshop_register, name="tuckshop_register"),
    path('view', views.product_list, name="product_list"),
    path('save-order/', views.save_order, name='save_order'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
