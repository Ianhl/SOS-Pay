from django.contrib import admin
from .models import UploadImageModel
from django.urls import path
from .views import *


admin.site.register(UploadImageModel)

urlpatterns =[
    path('media_upload', ImgUploadAPIview.as_view(), name="media_upload")
]