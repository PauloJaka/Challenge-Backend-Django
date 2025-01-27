from unittest.mock import Mock
from application.use_cases.list_transfers import ListTransfersUseCase
from datetime import datetime


def test_list_transfers_with_date_filter():
    repo_mock = Mock()

    transfers = [
        {"amount": 100, "date": datetime(2023, 10, 1)},
        {"amount": 200, "date": datetime(2023, 10, 2)},
    ]
    repo_mock.get_transfers.return_value = transfers

    use_case = ListTransfersUseCase(repo_mock)
    result = use_case.execute(
        cpf="12345678909", start_date="2023-10-01", end_date="2023-10-01"
    )

    assert len(result) == 1
    assert result[0]["amount"] == 100
