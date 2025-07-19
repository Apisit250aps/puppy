from rest_framework import serializers
from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            "id",
            "owner",
            "name",
            "type",
            "desc",
            "created_at",
            "updated_at",
        ]
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "wallet",
            "title",
            "desc",
            "type",
            "amount",
            "created_at",
            "updated_at",
        ]
        
    def validate_wallet(self, value):
        user = self.context['request'].user
        if value.owner != user:
            raise serializers.ValidationError("You do not own this wallet.")
        return value
