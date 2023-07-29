from typing import Any
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
import stripe
from django.conf import settings

# from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import templates
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status


# from fcm_django.models import FCMDevice,Message
from fcm_django.models import FCMDevice, messaging
import firebase_admin
from firebase_admin import credentials

stripe.api_key = settings.STRIPE_PRIVATE_KEY

#* =================== show products =================== *#
@api_view(["GET"])
def get_products(request):
    filterset = ProductFilter(
        request.GET, queryset=Product.objects.all().order_by("id")
    )
    # product = Product.objects.all()
    # print("product",filterset.data)
    serializer = ProductSerializer(filterset.qs, many=True)
    return Response(
        {
            "Products": serializer.data,
        }
    )

#* =================== show a single product =================== *#
@api_view(["GET"])
def get_product(request, pk):
    # product  = Product.objects.get(id = pk)
    product = get_object_or_404(
        Product, id=pk
    )  #! ------ adds the object not found logic ----!#
    # print("product",product)
    serializer = ProductSerializer(product, many=False)
    return Response({"id": serializer.data}, status=status.HTTP_200_OK)

#* =================== create a FCM device =================== *#
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_fcm_device(request):
    user = request.user
    data = request.data
    # product = data.get('product')

    fcm_token = data["fcm_token"]
    # fcm_token = data.get("fcm_token","Not present")
    if not fcm_token:
        return Response({"detail": "FCM token not provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        device  = FCMDevice()
        device.registration_id = fcm_token
        device.user = user
        device.save()
    except Exception as e:
        print("error creating FCM device",e)
    
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate('/Users/nischal/Documents/project/ProjectAdvisor/serviceaccountkey.json')
            firebase_admin.initialize_app(cred)
        device, created = FCMDevice.objects.update_or_create(
            user=user, defaults={"registration_id": fcm_token}
        )

    except IntegrityError:
        return Response({"detail": "This FCM token is already in use."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("error creating FCM device", e)
    return Response({'detail':'FCM device added and created successfully'},status=status.HTTP_201_CREATED)

#* =================== add a product =================== *#
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def add_product(request):
    user = request.user
    # print({"user":user})
    data = request.data
    # print(data)
    product = data["product"]

    for i in product:
        product = Product.objects.create(
            name=i["name"],
            description=i["description"],
            price=i["price"],
            user=user,
        )
        
        if not firebase_admin._apps:
            cred = credentials.Certificate('/Users/nischal/Documents/project/ProjectAdvisor/serviceaccountkey.json')
            firebase_admin.initialize_app(cred)
            
        devices = FCMDevice.objects.all()
        for device in devices:
            message = messaging.Message(
                data={
                    "title": "Product Added",
                    "body": f"a new product named {product.name} has been added to the database by {user.email} ",
                },
                notification=messaging.Notification(
                    title="Product Added",
                    body=f"a new product named {product.name} has been added to the database by {user.email} ",
                ),
                android=messaging.AndroidConfig(
                    priority="high",
                ),
                token = device.registration_id
            )
            device.send_message(message=message)
    serializer = ProductSerializer(product, many=False)
    # print(serializer.data)
    return Response(serializer.data)

#* =================== update a product =================== *##
@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    # if product.user != request.user:
    #     return Response({"Details":f"Permission-Denied current user {request.user.email} not allowed to perform the actions requested"},status=status.HTTP_401_UNAUTHORIZED)
    product.price = request.data["price"]
    product.description = request.data["description"]
    product.name = request.data["name"]
    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response({f"updated : {pk}": serializer.data})

#* =================== delete a product =================== *#
@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_product(request, pk):
    data = request.data
    user = request.user
    # product = Product.objects.get(id=pk)
    product = get_object_or_404(Product, id=pk)
    # if product.user != request.user:
    #     return Response({"Details":f"Permission-Denied current user {request.user.email} not allowed to perform the actions requested"},status=status.HTTP_401_UNAUTHORIZED)

    product.delete()
    return Response(
        {"product-details": {f"product for id  : {pk} deleted successfully"}},
        status=status.HTTP_204_NO_CONTENT,
    )


class ProductLandingPageView(TemplateView):
    template_name = "checkout.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(id=10)
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update(
            {
                "products": product,
                "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            }
        )
        return context


class CreateCheckoutSessionView(View):
    YOUR_DOMAIN = "http://localhost:8000"

    # def success(request):
    #     return render(request,"success.html")

    # def post(self,request,*args,**kwargs):
    #     checkout_session = stripe.checkout.Session.create(
    #         line_items=[
    #             {
    #                 # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
    #                 'price': 'price_1NPkztGvjAuWKVBt95bi330D',
    #                 'quantity': 1,
    #             },
    #         ],

    #         mode='payment',
    #         # mode='subscription',  # mode is of three types : payment , subscription , and setup #! ----------------------------------------------------------------------

    #         success_url=CreateCheckoutSessionView.YOUR_DOMAIN ,
    #         cancel_url=CreateCheckoutSessionView.YOUR_DOMAIN ,
    #     )
    #     # if checkout_session.id :
    #     #     return render(request,"success.html")
    #     # return JsonResponse({
    #     #     "id": checkout_session.id,
    #     #     "session":checkout_session
    #     # },)
    #     # response = redirect(checkout_session.url)
    #     # response.status_code = 303
    #     return redirect(checkout_session.url)
