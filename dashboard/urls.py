from django.urls import path
from .views import *

urlpatterns = [
    path("product_count/", all_product_count, name="product_count")
]
