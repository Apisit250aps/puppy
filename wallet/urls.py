from django.urls import path
from wallet import views

urlpatterns = [
    path("register", views.register_api, name="register-api"),
    path("login", views.login_api, name="login-api"),
     # Wallet CRUD
    path("wallets/", views.list_wallet, name="wallet-list"),
    path("wallets/<uuid:pk>/", views.retrieve_wallet, name="wallet-detail"),
    path("wallets/create/", views.create_wallet, name="wallet-create"),
    path("wallets/<uuid:pk>/update/", views.update_wallet, name="wallet-update"),
    path("wallets/<uuid:pk>/delete/", views.delete_wallet, name="wallet-delete"),
    # Transaction CRUD
    path("transactions/", views.list_transaction, name="transaction-list"),
    path("transactions/<uuid:pk>/", views.retrieve_transaction, name="transaction-detail"),
    path("transactions/create/", views.create_transaction, name="transaction-create"),
    path("transactions/<uuid:pk>/update/", views.update_transaction, name="transaction-update"),
    path("transactions/<uuid:pk>/delete/", views.delete_transaction, name="transaction-delete"),
]
