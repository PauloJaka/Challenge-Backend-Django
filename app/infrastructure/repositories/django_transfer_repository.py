from typing import List
from django.utils import timezone
from application.interfaces.transfer_repository_interface import TransferRepository
from domain.entities.transfer import Transfer
from infrastructure.models.transfer_model import DjangoTransfer

class DjangoTransferRepository(TransferRepository):
    def get_transfers(
        self,
        cpf: str,
        start_date: timezone.datetime = None,
        end_date: timezone.datetime = None,
    ) -> List[Transfer]:
        transfers = DjangoTransfer.objects.filter(source_cpf=cpf)
        
        if start_date:
            transfers = transfers.filter(date__gte=start_date)
        if end_date:
            transfers = transfers.filter(date__lte=end_date)
        
        return [
            Transfer(
                id=transfer.id,
                source_cpf=transfer.source_cpf,
                target_cpf=transfer.target_cpf,
                amount=transfer.amount,
                date=timezone.localtime(transfer.date),
            )
            for transfer in transfers
        ]