from django.urls import path
from .views import *

urlpatterns = [
    path("product_count/", all_product_count, name="product_count"),
    path("all_stock/", all_stock, name="all_stock"),
    path("low_stock/", low_stock_product, name="low_stock_product"),
    path("today_stock/", today_stock_in, name="today_stock_in"),
    path("all_stock_out/", all_stock_out, name="all_stock_out"),
    path("today_stock_out/", today_stock_out, name="today_stock_out")
    
]
