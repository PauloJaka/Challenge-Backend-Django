from typing import List
from django.utils import timezone
from application.interfaces.transfer_repository_interface import TransferRepository
from domain.entities.transfer import Transfer
from infrastructure.models.transfer_model import DjangoTransfer
from datetime import datetime

from django.utils import timezone


class DjangoTransferRepository(TransferRepository):
    def get_transfers(
        self,
        cpf: str,
        start_date: datetime = None,
        end_date: datetime = None,
    ) -> List[Transfer]:
        queryset = DjangoTransfer.objects.filter(source_cpf=cpf)

        # Filtragem por partes da data
        if start_date:
            if start_date.year:
                queryset = queryset.filter(date__year__gte=start_date.year)
            if start_date.month:
                queryset = queryset.filter(date__month__gte=start_date.month)
            if start_date.day:
                queryset = queryset.filter(date__day__gte=start_date.day)

        if end_date:
            if end_date.year:
                queryset = queryset.filter(date__year__lte=end_date.year)
            if end_date.month:
                queryset = queryset.filter(date__month__lte=end_date.month)
            if end_date.day:
                queryset = queryset.filter(date__day__lte=end_date.day)

        return [
            Transfer(
                id=transfer.id,
                source_cpf=transfer.source_cpf,
                target_cpf=transfer.target_cpf,
                amount=transfer.amount,
                date=timezone.localtime(transfer.date),
            )
            for transfer in queryset
        ]

    def save_transfer(
        self, source_cpf: str, target_cpf: str, amount: float, date: timezone.datetime
    ) -> Transfer:
        # Salvando a transferência no banco de dados
        transfer = DjangoTransfer.objects.create(
            source_cpf=source_cpf,
            target_cpf=target_cpf,
            amount=amount,
            date=date,
        )

        return Transfer(
            id=transfer.id,
            source_cpf=transfer.source_cpf,
            target_cpf=transfer.target_cpf,
            amount=transfer.amount,
            date=timezone.localtime(transfer.date),
        )
