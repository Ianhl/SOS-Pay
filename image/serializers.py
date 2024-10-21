from rest_framework import serializers
from .models import UploadImageModel


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImageModel
        fields = ('id', 'caption', 'image')