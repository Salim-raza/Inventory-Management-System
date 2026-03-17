from rest_framework import serializers
from .models import *

# create your serializers
class UserCreateSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ["email", "password", "role", "phone", "first_name", "last_name"]
        read_only_field = ["is_active", "is_staff", "is_superuser", "create_at", "update_at"]
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data["role"],
            phone=validated_data["phone"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )


class SigninSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
class ChangePasswordSerializers(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class CreateOtpSerializers(serializers.Serializer):
    email = serializers.EmailField()
    

class ResetPasswordSerializers(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()
    otp = serializers.CharField()
    