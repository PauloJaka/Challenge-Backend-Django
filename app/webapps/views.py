from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
import logging


# Use cases
from application.use_cases.transfer_funds import TransferFundsUseCase
from application.use_cases.list_transfers import ListTransfersUseCase
from application.use_cases.create_user import CreateUserUseCase
from application.use_cases.add_balance_to_wallet import AddBalanceToWalletUseCase
from application.use_cases.get_wallet_balance import GetWalletBalanceUseCase


# Repositories
from infrastructure.repositories.django_wallet_repository import DjangoWalletRepository
from infrastructure.repositories.django_transfer_repository import (
    DjangoTransferRepository,
)
from infrastructure.repositories.django_user_repository import DjangoUserRepository
from infrastructure.repositories.django_wallet_repository import DjangoWalletRepository


# Domain
from domain.exceptions.wallet_not_found_execption import WalletNotFoundException
from infrastructure.models import CustomUser
from domain.entities.user import User as DomainUser

# Utilities
from modules.utils.date_utils import parse_date


logger = logging.getLogger(__name__)


class CreateUserView(APIView):
    def post(self, request):
        data = request.data
        user_repository = DjangoUserRepository()

        validation_error = self.validate_user_data(data, user_repository)

        if validation_error:
            return Response(
                {"error": validation_error}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            wallet_repository = DjangoWalletRepository()
            use_case = CreateUserUseCase(user_repository, wallet_repository)

            user = use_case.execute(
                name=data["name"], cpf=data["cpf"], password=data["password"]
            )

            return Response(self.serialize_user(user), status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": f"Erro ao criar usuário: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def validate_user_data(data, user_repository):
        required_fields = ["name", "cpf", "password"]
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return f"Erro ao criar: falta {', '.join(missing_fields)}"

        if user_repository.get_by_cpf(data["cpf"]):
            return "Erro ao criar: já existe um usuário com esse CPF"

        return None

    @staticmethod
    def serialize_user(user: DomainUser):
        return {
            "id": user.id,
            "name": user.name,
            "cpf": user.cpf,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }


class WalletBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cpf = request.user.cpf  # CPF do usuário autenticado
            use_case = GetWalletBalanceUseCase(DjangoWalletRepository())
            balance = use_case.execute(cpf)
            return Response({"balance": balance}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=404)


class TransferFundsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        source_cpf = request.user.cpf
        target_cpf = request.data["target_cpf"]
        amount = float(request.data["amount"])

        transfer_repository = DjangoTransferRepository()

        use_case = TransferFundsUseCase(
            wallet_repository=DjangoWalletRepository(),
            transfer_repository=transfer_repository,
            notification_service=print("Transferencia inválida"),
        )

        use_case.execute(amount, source_cpf, target_cpf)

        return Response({"message": "Transferência realizada com sucesso."}, status=200)


class ListTransfersView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]
    page_size = 20

    def get(self, request):
        try:
            cpf = request.user.cpf
            logger.debug(f"Processando requisição para CPF: {cpf}")

            start_date_str = request.query_params.get("start_date")
            end_date_str = request.query_params.get("end_date")

            start_date = None
            end_date = None

            if start_date_str:
                start_date = parse_date(start_date_str)
                start_date = timezone.make_aware(start_date)

            if end_date_str:
                end_date = parse_date(end_date_str)
                end_date = timezone.make_aware(end_date)

            use_case = ListTransfersUseCase(DjangoTransferRepository())
            transfers = use_case.execute(cpf, start_date, end_date)

            if not transfers:
                return Response(status=status.HTTP_204_NO_CONTENT)

            # Paginação e serialização
            page = self.paginate_queryset(transfers, request)
            if page is not None:
                transfers_data = [
                    {
                        "id": transfer.id,
                        "source_cpf": transfer.source_cpf,
                        "target_cpf": transfer.target_cpf,
                        "amount": float(transfer.amount),
                        "date": transfer.date.isoformat(),
                    }
                    for transfer in page
                ]
                return self.get_paginated_response(transfers_data)

            return Response(
                {"message": "No transfers found"}, status=status.HTTP_204_NO_CONTENT
            )

        except ValueError as e:
            logger.error(f"Erro de formato de data: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erro interno: {str(e)}", exc_info=True)
            return Response(
                {"error": "Erro interno no servidor"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AddBalanceToWalletView(APIView):
    def post(self, request, cpf):
        try:
            amount = float(request.data.get("amount", 0))
            use_case = AddBalanceToWalletUseCase(DjangoWalletRepository())
            wallet = use_case.execute(cpf, amount)
            return JsonResponse({"balance": wallet.balance}, status=200)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except WalletNotFoundException as e:
            return JsonResponse({"error": "Carteira não encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Carteira não encontrada"}, status=404)
