from rest_framework.decorators import api_view, permission_classes, authentication_classes
from inventory.serializers import ProductCreateSerializers, StockInSerializers, StockOutSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from inventory.models import Product, StockIn, StockOut
from rest_framework.response import Response
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from django.db.models import F
from accounts.permision import *
from datetime import timedelta

# Create your views here.

@swagger_auto_schema(
    method="GET",
    responses= {200: ProductCreateSerializers(many=True)},
    operation_description="all product count"
)
@api_view(["GET"])
@permission_classes([IsAdmin])
@authentication_classes([JWTAuthentication])
def all_product_count(request):
    products = Product.objects.all()
    
    data = {
        "total products": products.count(),
        "products": ProductCreateSerializers(products, many=True).data
    }
    return Response(data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method="GET",
    responses= {200: StockInSerializers(many=True)},
    operation_description="all stock"
)
@api_view(["GET"])
@permission_classes([IsAdminORManager])
@authentication_classes([JWTAuthentication])
def all_stock(request):
    stock = StockIn.objects.all()
    
    data = {
        "total stock": stock.count(),
        "stocks": StockInSerializers(stock, many=True).data
    }
    
    return Response(data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="GET",
    responses= {200: ProductCreateSerializers(many=True)},
    operation_description="low stock product"
)

@api_view(["GET"])
@permission_classes([IsAdminORManager])
@authentication_classes([JWTAuthentication])
def low_stock_product(request):
    low_stock = Product.objects.filter(
        current_stock__lt=F("minimum_stock_level")
    )
    
    
    data = {
        "total low stock": low_stock.count(),
        "low stock": ProductCreateSerializers(low_stock, many=True).data
    }
    
    return Response(data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method="GET",
    responses= {200: StockInSerializers(many=True)},
    operation_description="today stock in"
)
@api_view(["GET"])
@permission_classes([IsAdminORManager])
@authentication_classes([JWTAuthentication])
def today_stock_in(request):
    start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    today_stock = StockIn.objects.filter(
        create_at__gt=start,
        create_at__lt=end
    )
    
    data = {
        "total stock today": today_stock.count(),
        "today stock": StockInSerializers(today_stock, many=True).data
    }
    
    return Response(data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method="GET",
    responses= {200: StockOutSerializers(many=True)},
    operation_description="all stock out"
)
@api_view(["GET"])
@permission_classes([IsAdminORManager])
@authentication_classes([JWTAuthentication])
def all_stock_out(request):
     stock_out = StockOut.objects.all()
     
     data = {
         "total stock out": stock_out.count(),
         "stock out": StockOutSerializers(stock_out, many=True).data
     }
     
     return Response(data , status=status.HTTP_200_OK)

@swagger_auto_schema(
    method="GET",
    responses= {200: StockOutSerializers(many=True)},
    operation_description="today stock out"
)
@api_view(["GET"])
@permission_classes([IsAdminORManager])
@authentication_classes([JWTAuthentication])
def today_stock_out(request):
    start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    stock_out = StockOut.objects.filter(
        create_at__gt=start,
        create_at__lt=end
    )
    
    data = {
        "today stock out": stock_out.count(),
        "stock out": StockOutSerializers(stock_out, many=True).data
    }
    
    return Response(data, status=status.HTTP_200_OK)