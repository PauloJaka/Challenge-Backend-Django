class InsufficientBalanceError(Exception):
    """
    Exceção lançada quando uma operação tenta reduzir o saldo de uma carteira
    abaixo do valor permitido.
    """

    def __init__(self, message="Saldo insuficiente para realizar a operação"):
        self.message = message
        super().__init__(self.message)
