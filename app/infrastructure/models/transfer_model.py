from django.db import models
from django.contrib.auth import get_user_model


class DjangoTransfer(models.Model):
    source_cpf = models.CharField(max_length=11)
    target_cpf = models.CharField(max_length=11)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transferência de {self.source_cpf} para {self.target_cpf}"
