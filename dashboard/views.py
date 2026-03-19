from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from inventory.serializers import ProductCreateSerializers
from rest_framework.response import Response
from inventory.models import Product
from rest_framework import status
from accounts.permision import *

# Create your views here.
@api_view(["GET"])
@permission_classes([IsAdmin])
@authentication_classes([JWTAuthentication])
def all_product_count(request):
    products = Product.objects.all()
    
    data = {
        "total_products": products.count(),
        "products": ProductCreateSerializers(products, many=True).data
    }
    
    return Response(data)
    https://github.com/Salim-raza/Inventory-Management-System