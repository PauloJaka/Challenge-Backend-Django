from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from domain.entities.transfer import Transfer


class TransferRepository(ABC):
    @abstractmethod
    def get_transfers(
        self,
        cpf: str,
        start_date: datetime = None,
        end_date: datetime = None,
    ) -> List[Transfer]:
        pass
