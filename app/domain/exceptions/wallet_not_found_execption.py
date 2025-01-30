class WalletNotFoundException(Exception):
    def __init__(self, message="Carteira não encontrada"):
        self.message = message
        super().__init__(self.message)
