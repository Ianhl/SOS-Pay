from django.shortcuts import render
from rest_framework.response import Response
from .serializers import UploadImageSerializer
from rest_framework import status
from .models import UploadImageModel
from rest_framework.views import APIView

# Create your views here.

class ImgUploadAPIview(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        qs_serializer = UploadImageSerializer(
            data={
                "caption": request.data.get("caption"),
                
            }
        )