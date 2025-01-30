from unittest.mock import Mock
from datetime import datetime
from application.use_cases.list_transfers import ListTransfersUseCase
from domain.entities.transfer import Transfer

def test_list_transfers_without_filters():
    transfer_repo = Mock()
    transfer_repo.get_transfers.return_value = [
        Transfer(
            id=1,
            source_cpf="12345678909",
            target_cpf="98765432100",
            amount=100.0,
            date=datetime(2023, 10, 1),
        )
    ]

    use_case = ListTransfersUseCase(transfer_repo)
    transfers = use_case.execute("12345678909")

    assert len(transfers) == 1
    assert transfers[0].source_cpf == "12345678909"
    transfer_repo.get_transfers.assert_called_once_with("12345678909", None, None)

def test_list_transfers_with_date_filters():
    transfer_repo = Mock()
    transfer_repo.get_transfers.return_value = [
        Transfer(
            id=1,
            source_cpf="12345678909",
            target_cpf="98765432100",
            amount=100.0,
            date=datetime(2023, 10, 1),
        )
    ]

    use_case = ListTransfersUseCase(transfer_repo)
    transfers = use_case.execute(
        cpf="12345678909",
        start_date="2023-10-01",
        end_date="2023-10-31",
    )

    assert len(transfers) == 1
    transfer_repo.get_transfers.assert_called_once_with(
        "12345678909",
        "2023-10-01",
        "2023-10-31",
    )