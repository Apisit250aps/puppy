from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

WALLET_TYPES = (
    (0, "mix"),
    (1, "cash"),
    (2, "bank"),
)

TRANSACTION_TYPES = (
    (-1, "expended"),
    (1, "income"),
)


# Create your models here.
class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username


class Wallet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    type = models.IntegerField(choices=WALLET_TYPES, default=0)
    desc = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    desc = models.TextField()
    type = models.IntegerField(choices=TRANSACTION_TYPES, default=1)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} : {self.amount}"
