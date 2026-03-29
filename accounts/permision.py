from rest_framework.permissions import IsAuthenticated
from .models import *

class IsSales(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role == "sales"
    
class IsManager(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role == "manager"


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role == "admin"
    
class IsAdminORManager(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role == "admin" or user.role == "manager"



class IsManagerORSales(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role == "manager" or user.role == "sales"
    
