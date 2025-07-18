# django
from django.shortcuts import render
from django.contrib.auth import authenticate

# rest framework
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    # client error
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    # Server error
    HTTP_500_INTERNAL_SERVER_ERROR,
)

# models
from .models import User

# utils
from .utils import ApiResponse


# Create your views here.
@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(req: Request):
    try:
        username = req.data.get("username")
        password = req.data.get("password")

        if not username or not password:
            return ApiResponse.json(
                "Username and password are required",
                success=False,
                status=HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(username=username).exists():
            return ApiResponse.json(
                "Username already exists", success=False, status=HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return ApiResponse.json(
            "Register successful",
            success=True,
            data={"user_id": user.id},
            status=HTTP_201_CREATED,
        )

    except Exception as e:
        return ApiResponse.json(
            f"Error: {str(e)}", success=False, status=HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def login_api(req: Request):
    try:
        username = req.data.get("username")
        password = req.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return ApiResponse.json(
                "Invalid username or password",
                success=False,
                status=HTTP_401_UNAUTHORIZED,
            )

        # ตัวอย่าง: return user id (ถ้าไม่มี token system)
        return ApiResponse.json(
            "Login successful",
            success=True,
            data={"user_id": user.id},
            status=HTTP_200_OK,
        )

    except Exception as e:
        return ApiResponse.json(
            f"Error: {str(e)}", success=False, status=HTTP_500_INTERNAL_SERVER_ERROR
        )
