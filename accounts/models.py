from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .usermanager import *
import datetime


class CustomUser(AbstractUser):
    ROLE_CHOICE = [
        ('admin', 'ADMIN'),
        ('manager', 'MANAGER'),
        ('sales', 'SALES')
    ]
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICE, default='SALES')
    phone = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role == 'ADMIN'
    
    @property
    def is_manager(self):
        return self.role == 'MANAGER'
    
    @property
    def is_sales(self):
        return self.role.lower() == 'SALES'
    
    
    
class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField()
    create_at = models.DateTimeField(auto_now_add=True)
    
    
    def is_expire(self):
        return self.create_at + timezone.now() + datetime.timedelta(minutes=5) > timezone.now()
