from rest_framework import serializers
from .models import Product


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'image']
        
    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance