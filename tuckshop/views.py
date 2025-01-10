from django.shortcuts import redirect, render
from django.urls import reverse
from .decorator import user_is_tuckshop_owner
from rest_framework.response import Response
from .serializers import ProductImageSerializer
from rest_framework import status
from .models import Product
from rest_framework.views import APIView
from urllib.parse import urlencode
from django.http import JsonResponse
from .models import Product, Order, OrderItem
import json
# Create your views here.

@user_is_tuckshop_owner
def tuckshop_main(request):
    return render(request, "tuckshop/index.html")

def product_list(request):
     # Fetch all products, including their image fields
    products = Product.objects.all()

    return render(request, "tuckshop/index.html", {'products': products})


def tuckshop_register(request):
    if request.method == "POST":
        product_name = request.POST['product_name']
        product_category = request.POST['product_category']
        price = request.POST['price']
        
        product = Product.objects.create(
            product_name = product_name,
            product_category = product_category,
            price = price,
        )
        product.save()
        product_id = product.product_id
        
        query_params = urlencode({'product_id': product_id})
        redirect_url = f"{reverse('media_upload')}?{query_params}"
        
        return redirect(redirect_url)
       
    return render(request, "tuckshop/form.html")


class ImgUploadAPIview(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        product_id = request.data.get("product_id")
        image = request.FILES.get("media")
        
        if not product_id:
            return Response({"message": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not image:
            return Response({"message": "Image file is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found", "data": None},
                status=status.HTTP_404_NOT_FOUND,
            )
            
        product.image = image
        
        product.save()
        
        return Response(
            {
                "message": "Media uploaded successfully",
                "data": {
                    "product_id": product.product_id,
                    "image_url": product.image.url,  # Return image URL as response
                },
            },
            status=status.HTTP_200_OK,
        )
        
        
        # qs_serializer = UploadImageSerializer(
        #     data={
        #         "product_id": product_id,
        #         "image": request.FILES.get("media"),
        #     },
            
        #     context={"request":request}
        # )
        
        # if qs_serializer.is_valid():
        #     qs_serializer.save()
        #     return Response(
        #         {
        #         "message": "Media uploaded successfully",
        #         "data": qs_serializer.data,
        #     },
        #         status=status.HTTP_200_OK,
        #     )
        # else:
        #     return Response(
        #         {"message": qs_serializer.errors, "data":None},
        #         status=status.HTTP_400_BAD_REQUEST,
                
                
        #     )
    def get(self, request):
        # qs = UploadImageModel.objects.all()
        # qs_serializer = UploadImageSerializer(qs, many=True)
        # return Response(qs_serializer.data, status=status.HTTP_400_BAD_REQUEST)
        product_id = request.GET.get('product_id')
        context = {"product_id": product_id}
        return render(request, 'image/index.html')
    
def save_order(request):
    if request.method == "POST":
        try:
            # Parse the incoming JSON data
            order_data = json.loads(request.body)

            # Output the parsed data to the server console
            print("Order Data Received:", order_data)

            # Create a new Order
            order = Order.objects.create()

            for item in order_data['items']:
                try:
                    product = Product.objects.get(product_id=item['product_id'])
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity']
                    )
                except Product.DoesNotExist:
                    return JsonResponse({'message': f"Product with ID {item['product_id']} not found"}, status=404)
                except Exception as e:
                    print(f"Error creating OrderItem: {str(e)}")
                    return JsonResponse({'message': f'Error creating OrderItem: {str(e)}'}, status=500)

            return JsonResponse({'message': 'Order saved successfully', 'order_id': order.id})

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            print(f"Error processing order: {str(e)}")
            return JsonResponse({'message': f'Error processing order: {str(e)}'}, status=500)

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    products = Product.objects.all()
    return render(request, 'tuckshop/checkout.html', {'order': order, 'products':products,})


def checkout(request):
    return render(request, 'tuckshop/checkout.html')