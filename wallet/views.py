# django
from django.shortcuts import render
from django.contrib.auth import authenticate

# rest framework
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    # client error
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    # Server error
    HTTP_500_INTERNAL_SERVER_ERROR,
)

# models
from .models import User, Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer

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


@api_view(["GET"])
@permission_classes([AllowAny])
def list_wallet(request):
    wallets = Wallet.objects.all()
    serializer = WalletSerializer(wallets, many=True)
    return ApiResponse.json("Wallet list", True, serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def retrieve_wallet(request, pk):
    try:
        wallet = Wallet.objects.get(pk=pk)
    except Wallet.DoesNotExist:
        return ApiResponse.json("Wallet not found", False, status=HTTP_404_NOT_FOUND)

    serializer = WalletSerializer(wallet)
    return ApiResponse.json("Wallet retrieved", True, serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_wallet(request):
    serializer = WalletSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return ApiResponse.json("Wallet created", True, serializer.data, status=201)
    return ApiResponse.json(
        "Validation error", False, serializer.errors, status=HTTP_400_BAD_REQUEST
    )


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_wallet(request, pk):
    try:
        wallet = Wallet.objects.get(pk=pk)
    except Wallet.DoesNotExist:
        return ApiResponse.json("Wallet not found", False, status=HTTP_404_NOT_FOUND)

    serializer = WalletSerializer(wallet, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return ApiResponse.json("Wallet updated", True, serializer.data)
    return ApiResponse.json(
        "Validation error", False, serializer.errors, status=HTTP_400_BAD_REQUEST
    )


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_wallet(request, pk):
    try:
        wallet = Wallet.objects.get(pk=pk)
    except Wallet.DoesNotExist:
        return ApiResponse.json("Wallet not found", False, status=HTTP_404_NOT_FOUND)
    wallet.delete()
    return ApiResponse.json("Wallet deleted", True, status=HTTP_204_NO_CONTENT)


# TRANSACTION CRUD


@api_view(["GET"])
@permission_classes([AllowAny])
def list_transaction(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    return ApiResponse.json("Transaction list", True, serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def retrieve_transaction(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return ApiResponse.json(
            "Transaction not found", False, status=HTTP_404_NOT_FOUND
        )

    serializer = TransactionSerializer(transaction)
    return ApiResponse.json("Transaction retrieved", True, serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return ApiResponse.json(
            "Transaction created", True, serializer.data, status=201
        )
    return ApiResponse.json(
        "Validation error", False, serializer.errors, status=HTTP_400_BAD_REQUEST
    )


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_transaction(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return ApiResponse.json(
            "Transaction not found", False, status=HTTP_404_NOT_FOUND
        )

    serializer = TransactionSerializer(transaction, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return ApiResponse.json("Transaction updated", True, serializer.data)
    return ApiResponse.json(
        "Validation error", False, serializer.errors, status=HTTP_400_BAD_REQUEST
    )


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_transaction(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return ApiResponse.json(
            "Transaction not found", False, status=HTTP_404_NOT_FOUND
        )

    transaction.delete()
    return ApiResponse.json("Transaction deleted", True, status=HTTP_204_NO_CONTENT)
