# mpesa_client/urls.py
from django.urls import path
from .views import  confirm_payment

urlpatterns = [
    path('/payments/confirmation/', confirm_payment, name='confirm_payment'),
]
