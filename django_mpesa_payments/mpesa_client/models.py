from django.db import models

# model to store transaction details .
class MpesaTransaction(models.Model):
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    transaction_date = models.DateTimeField()
    status = models.CharField(max_length=50)
    additional_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.transaction_id
