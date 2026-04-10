from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import authenticate
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from .serializers import *
from .utils import *
import random


# create your view
@swagger_auto_schema(
    method='post',
    request_body=UserCreateSerializers,
    responses={201: UserCreateSerializers(many=False), 400: 'Bad Request'},
    operation_description="create a new user"
)
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializers = UserCreateSerializers(data=request.data)
    if serializers.is_valid():
        user = serializers.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({
                "user": UserCreateSerializers(user).data,
                "token": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)

    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=SigninSerializers,
    responses={201: SigninSerializers(many=False), 400: 'Bad Request'},
    operation_description="login user"
)
@api_view(["POST"])
@permission_classes([AllowAny])
def signin(request):
    serializers = SigninSerializers(data=request.data)
    serializers.is_valid(raise_exception=True)
    user = authenticate(
        email=serializers.validated_data["email"],
        password=serializers.validated_data["password"]
    )
    if user is not None:
        token = get_tokens_for_user(user)
        return Response({"message": "Login Successfully .", "access_token" : token["access"], "refresh_token": token["refresh"]}, status=status.HTTP_200_OK)
    return Response({"message" : "Invalid Email Or Password"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=ChangePasswordSerializers,
    responses={201: ChangePasswordSerializers(many=False), 400: 'Bad Request'},
    operation_description="change password"
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def change_password(request):
    serializers = ChangePasswordSerializers(data=request.data)
    serializers.is_valid(raise_exception=True)
    
    user = get_object_or_404(CustomUser, id=request.user.id)
    if user.check_password(serializers.validated_data["old_password"]):
        user.set_password(serializers.validated_data["new_password"])
        user.save()
        return Response({"message": "Password Change Successfully ."}, status=status.HTTP_200_OK)
    return Response({"message": "Invalid Old Password"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=CreateOtpSerializers,
    responses={201: CreateOtpSerializers(many=False), 400: 'Bad Request'},
    operation_description="create otp"
)
@api_view(["POST"])
@permission_classes([AllowAny])
def send_otp(request):
    serializers = CreateOtpSerializers(data=request.data)
    serializers.is_valid(raise_exception=True)
    
    email = serializers.validated_data['email']
    
    if CustomUser.objects.filter(email=email).exists():
        user = CustomUser.objects.get(email=email)
        otp = random.randint(1111, 9999)
        
        OTP.objects.update_or_create(user=user, defaults={'otp': otp})
        
        
        plain_message = f"This is plain message. Your OTP is {otp}. id will expire in 5 minutes."
        
        
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background:#f9f9f9; padding:20px;">
        <div style="max-width:600px; margin:auto; background:white; padding:20px; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1);": <h2 style="color:#333;">Password Reset OTP</h2>
        <p>Hello {email},</p>
        <p>Your One-Time Password (OTP) is:</p>
        <h1 style="color:#007bff; letter-spacing:5px;">{otp}</h1>
        <p>This code is valid for <b>5 minutes</b>. Do not share it with anyone.</p>
        <p style="font-size:12px; color:#888;">If you didn't request this, please ignore this email.</p>
        </div>
        </body> </html>
        """
        
        send_mail(
            subject="Reset Password OTP",
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[serializers.validated_data['email']],
            fail_silently=False,
            html_message=html_message
        )
        
        return Response({
            "status": "Success",
            "message": "OTP Send Successfully To Your Gmail",
        }, status=status.HTTP_201_CREATED)
        
    return Response({
        "status": "failed",
        "message": "email doesnot exists"
    },status=status.HTTP_400_BAD_REQUEST)
    

@swagger_auto_schema(
    method='post',
    request_body=ResetPasswordSerializers,
    responses={201: ResetPasswordSerializers(many=False), 400: 'Bad Request'},
    operation_description="reset password"
)
@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    serializers = ResetPasswordSerializers(data=request.data)
    serializers.is_valid(raise_exception=True)
    
    email = serializers.validated_data["email"]
    otp = serializers.validated_data["otp"]
    new_password = serializers.validated_data["new_password"]
    
    
    if CustomUser.objects.filter(email=email).exists():
        user = CustomUser.objects.get(email_iexact=email)
        db_otp = OTP.objects.filter(user=user).last()
        
        
        if str(otp) == str(db_otp.otp):
            if not db_otp.is_expire:
                return Response({
                    "status" : "error",
                    "message" : "otp time expired"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.save()

            return Response({
                "status": "success",
                "message": "Password Reset Successfully."
            }, status=status.HTTP_200_OK)
            
    
        return Response({
            "status": "failed",
            "message": "Wrong otp."
        }, status=status.HTTP_400_BAD_REQUEST)
        
    return Response({
        "status": "failed",
        "message": "email dosenot exists."
    }, status=status.HTTP_400_BAD_REQUEST)
