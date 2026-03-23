from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .tasks import low_stock_alert, stock_in_alert
from rest_framework import status
from accounts.permision import *
from .serializers import *

# Create your views here.

@swagger_auto_schema(
    method='post',
    request_body=CreateCategorySerializers,
    responses={201: CreateCategorySerializers(many=False), 400: 'Bad Request'},
    operation_description="create category"
)
@api_view(["POST"])
@permission_classes([IsAdminORManager])
@authentication_classes([JWTAuthentication])
def create_category(request):
    serializers = CreateCategorySerializers(data=request.data)
    serializers.is_valid(raise_exception=True)
    serializers.save()
    return Response(serializers.data, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='GET',
    responses={200: ProductCreateSerializers(many=True)},
    operation_description="get all product"
)
@swagger_auto_schema(
    method='POST',
    request_body= ProductCreateSerializers,
    responses={201: ProductCreateSerializers(many=False), 400: 'Bad Request'},
    operation_description="create product"
)
@api_view(["GET", "POST"])
@permission_classes([IsAdminORManager, IsSales])
@authentication_classes([JWTAuthentication])
def product(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductCreateSerializers(products, many=True)
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)
    
    if request.method == "POST":
        serializer = ProductCreateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response({
            "product": ProductCreateSerializers(product).data 
        }, status=status.HTTP_201_CREATED)
    
    
@swagger_auto_schema(
    method='DELETE',
    responses={200: 'Delete product', 404: 'Not Found'},
    operation_description="delete product"  
)
@swagger_auto_schema(
    method='PATCH',
    request_body= UpdateProductSerializers,
    responses={200: UpdateProductSerializers(many=False), 400: 'Bad Request'},
    operation_description="update product"
)
@api_view(["PATCH", "DELETE"])
@permission_classes([IsAdminORManager])
@authentication_classes([JWTAuthentication])
def update_delete(request, id):
    if request.method == "PATCH":
        product = get_object_or_404(Product, id=id)
        serializers = UpdateProductSerializers(product, data=request.data, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({"product": serializers.data}, status=status.HTTP_200_OK)

    if request.method == "DELETE":
        product = get_object_or_404(Product, id=id, owner=request.user)
        product.delete()
        return Response({"message": "product delete successfully ."}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="GET",
    responses={200: CreateWarehouseSerializers(many=True)},
    operation_description="get all warehouse"
)
@swagger_auto_schema(
    method='POST',
    request_body= CreateWarehouseSerializers,
    responses={201: CreateWarehouseSerializers(many=False), 400: 'Bad Request'},
    operation_description="get and create warehouse"
)
@api_view(["GET", "POST"])
@permission_classes([IsAdminORManager])
@authentication_classes([JWTAuthentication])
def warehouse(request):
    if request.method == "GET":
        warehouse = Warehouse.objects.all()
        serializers = CreateWarehouseSerializers(warehouse, many=True)
        return Response({"warehouse" : serializers.data}, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializers = CreateWarehouseSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({"message": "warehouser create successfully"}, status=status.HTTP_201_CREATED)
    
@swagger_auto_schema(
    method='PATCH',
    request_body= UpdateWarehouseSerializers,
    responses={201: UpdateWarehouseSerializers(many=False), 400: 'Bad Request'},
    operation_description="update warehouse"
)
@swagger_auto_schema(
    method='DELETE',
    responses={200: "delete warehouse", 400: 'Bad Request'},
    operation_description="delete warehouse"
)
@api_view(["PATCH", "DELETE"])
@permission_classes([IsAdminORManager])
@authentication_classes([JWTAuthentication])
def warehouser_modify(request, id):
    if request.method == "PATCH":
        warehouse = get_object_or_404(Warehouse, id=id)
        serializers = UpdateWarehouseSerializers(warehouse, data=request.data, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({"warehouse": serializers.data}, status=status.HTTP_200_OK)
    
    
    if request.method == "DELETE":
        warehouse = get_object_or_404(Warehouse, id=id)
        warehouse.delete()
        return Response({"message": "warehouse delete successful"}, status=status.HTTP_200_OK)
        
@swagger_auto_schema(
    method='POST',
    request_body= StockInSerializers,
    responses={201: StockInSerializers(many=False), 400: 'Bad Request'},
    operation_description="stock in"
)        
@api_view(["POST"])
@permission_classes([IsAdminORManager])
@authentication_classes([JWTAuthentication])
def stock_in(request):
    serializers =  StockInSerializers(data=request.data)
    serializers.is_valid(raise_exception=True)
    stock = serializers.save()
    product = stock.product
    product.current_stock += stock.quantity
    product.save()
    stock_in_alert.delay(stock.id)
    return Response({"message": "stock in successfully", "stock_in": serializers.data}, status=status.HTTP_201_CREATED)



@swagger_auto_schema(
    method='PATCH',
    request_body= StockUpdateSerializers,
    responses={201: StockUpdateSerializers(many=False), 400: 'Bad Request'},
    operation_description="stock_in update"
)
@api_view(["PATCH"])
@permission_classes([IsAdminORManager])
@authentication_classes([JWTAuthentication])
def Stock_modify(request, id):
    if request.method == "PATCH":
        stock = get_object_or_404(StockIn, id=id)
        product = stock.product
        old_quantity = stock.quantity
        serializer = StockUpdateSerializers(stock, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        stock.refresh_from_db()
        new_quantity = stock.quantity
        difference = new_quantity - old_quantity
        product.current_stock += difference
        product.save()

        return Response(
            {"message": "Stock updated successfully"},
            status=status.HTTP_200_OK
        )
    
@swagger_auto_schema(
    method="GET",
    responses={200: StockOutSerializers(many=True)},
    operation_description="get all stock out"
)

@swagger_auto_schema(
    method='POST',
    request_body= StockOutSerializers,
    responses={201: StockOutSerializers(many=False), 400: 'Bad Request'},
    operation_description="stock out"
)   
@api_view(["GET", "POST"])
@permission_classes([IsAdminORManager | IsSales])
@authentication_classes([JWTAuthentication])
def stock_out(request):
    if request.method == "GET":
        stock_out = StockOut.objects.all()
        stock = StockOutSerializers(stock_out, many=True)
        return Response({"message": "stock out all", "stock_out": stock.data}, status=status.HTTP_200_OK)
    
    if request.method == "POST":
        serializers = StockOutSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        low_stock_alert.delay()
        return Response({"message": "Stock Out Successfully"}, status=status.HTTP_200_OK)
    

@swagger_auto_schema(
    method='PATCH',
    request_body= StockOutSerializers,
    responses={201: StockOutSerializers(many=False), 400: 'Bad Request'},
    operation_description="stock out"
)   
@api_view(["PATCH"])
@permission_classes([IsAdminORManager | IsSales])
@authentication_classes([JWTAuthentication])
def stock_out_update(request, id):
        stock_out = get_object_or_404(StockOut, id=id)
        serializers = StockOutUpdateSerializers(stock_out, data=request.data, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({"message": "stock out update successful", "stock_out": serializers.data}, status=status.HTTP_200_OK)
        
    
    
#


