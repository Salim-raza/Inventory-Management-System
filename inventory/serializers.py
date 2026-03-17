from rest_framework import serializers
from .models import *



class CreateCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["create_at"]
        
class ProductCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "category", "price", "cost_price", "image"]
        read_only_fields = ["qr_code", "barcode", "minimum_stock_level", "created_at", "update_at"]
        
class UpdateProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "price"]


class CreateWarehouseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"
        read_only_fields = ["create_at", "update_at"]

class UpdateWarehouseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["name", "location"]
        read_only_fields = ["create_at", "update_at"]

    
class StockInSerializers(serializers.ModelSerializer):
    product_details = ProductCreateSerializers(read_only=True)
    
    class Meta:
        model = StockIn
        fields = "__all__"
        read_only_fields = ["total_price", "create_at", "last_update"]
        
class StockUpdateSerializers(serializers.ModelSerializer):
    product = ProductCreateSerializers(read_only=True)
    class Meta:
        model = StockIn
        fields = "__all__"
        read_only_fields = ["create_at", "last_update"]
        
class StockOutSerializers(serializers.ModelSerializer):
    stock = StockInSerializers(read_only=True)
    class Meta:
        model = StockOut
        fields = "__all__"
        read_only_fields = ["create_at", "update_at"]
        
class StockOutUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = StockOut
        fields = "__all__"
        read_only_fields = ["create_at", "update_at"]