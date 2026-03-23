from django.urls import path
from .views import *


urlpatterns = [
    path("create_category/", create_category, name="create_category"),
    path("product/", product, name="product"),
    path("update<int:id>/", update_delete, name="update_product"),
    path("delete<int:id>/", update_delete, name="delete"),
    path("warehouse/", warehouse, name="warehouse"),
    path("warehouser_modify/<int:id>/", warehouser_modify, name="warehouser_modify"),
    path("stock_in/", stock_in, name="stock_in"),
    path("stock_modify/<int:id>/", Stock_modify, name="Stock_modify"),
    path("stock_out/", stock_out, name="stock_out"),
    path("stock_out_modify/<int:id>/", stock_out_update, name="stock_modify/")
]