class GetWalletBalanceUseCase:
    def __init__(self, wallet_repository):
        self.wallet_repository = wallet_repository

    def execute(self, cpf: str) -> float:
        wallet = self.wallet_repository.get_wallet(cpf)
        return wallet.balance
