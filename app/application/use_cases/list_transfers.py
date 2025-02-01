from typing import List
from domain.entities.transfer import Transfer
from application.interfaces.transfer_repository_interface import TransferRepository


class ListTransfersUseCase:
    def __init__(self, transfer_repository: TransferRepository):
        self.transfer_repository = transfer_repository

    def execute(
        self,
        cpf: str,
        start_date: str = None,
        end_date: str = None,
    ) -> List[Transfer]:
        return self.transfer_repository.get_transfers(cpf, start_date, end_date)
