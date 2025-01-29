from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from application.use_cases.transfer_funds import TransferFundsUseCase
from infrastructure.repositories.django_wallet_repository import DjangoWalletRepository

class TransferFundsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        source_cpf = request.user.cpf  
        target_cpf = request.data["target_cpf"]
        amount = float(request.data["amount"])

        use_case = TransferFundsUseCase(
            wallet_repository=DjangoWalletRepository(),
            notification_service=print("Transferencia inválida")
        )
        use_case.execute(amount, source_cpf, target_cpf)

        return Response({"message": "Transferência realizada com sucesso."}, status=200)