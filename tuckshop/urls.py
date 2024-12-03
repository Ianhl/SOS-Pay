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
    path('view', views.product_list, name="product_list")
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
