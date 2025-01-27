from django.utils import timezone
from core.entities.wallet import Wallet as CoreWallet
from app.infrastructure.models.models import Wallet as DjangoWallet
from django.contrib.auth import get_user_model


class DjangoWalletRepository:
    def get_wallet(self, cpf: str) -> CoreWallet:
        django_user = get_user_model().objects.get(cpf=cpf)
        django_wallet = DjangoWallet.objects.get(cpf=django_user)
        created_at_brazil = timezone.localtime(django_wallet.created_at)
        last_transaction_brazil = timezone.localtime(
            django_wallet.last_transaction_date
        )
        return CoreWallet(
            id=django_wallet.id,
            cpf=django_user.cpf,
            balance=django_wallet.balance,
            created_at=created_at_brazil,
            last_transaction_date=last_transaction_brazil,
        )

    def save(self, wallet: CoreWallet) -> CoreWallet:
        django_user = get_user_model().objects.get(cpf=wallet.cpf)
        django_wallet, _ = DjangoWallet.objects.update_or_create(
            cpf=django_user,
            defaults={
                "balance": wallet.balance,
                "last_transaction_date": wallet.last_transaction_date,
            },
        )
        return CoreWallet(
            id=django_wallet.id,
            cpf=django_user.cpf,
            balance=django_wallet.balance,
            created_at=timezone.localtime(django_wallet.created_at),
            last_transaction_date=timezone.localtime(
                django_wallet.last_transaction_date
            ),
        )
