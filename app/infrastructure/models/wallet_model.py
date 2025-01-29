from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class DjangoWallet(models.Model):
    id = models.AutoField(primary_key=True)
    cpf = models.OneToOneField(
        get_user_model(),
        to_field="cpf",
        on_delete=models.CASCADE,
        unique=True
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_transaction_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet {self.cpf}"

    class Meta:
        db_table = 'wallet'