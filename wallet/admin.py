from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Wallet, Transaction


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "type", "created_at", "updated_at")
    search_fields = ("name", "owner__username")
    list_filter = ("type", "created_at")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "wallet",
        "type",
        "amount",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "wallet__name")
    list_filter = ("type", "created_at")
