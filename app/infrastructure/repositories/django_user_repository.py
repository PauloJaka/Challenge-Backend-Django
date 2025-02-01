from django.contrib.auth import get_user_model
from django.utils import timezone
from domain.entities.user import User as DomainUser


class DjangoUserRepository:
    def save(self, user: DomainUser) -> DomainUser:
        DjangoUser = get_user_model()

        if not user.password:
            raise ValueError("A senha é obrigatória.")

        django_user = DjangoUser(
            cpf=user.cpf,
            name=user.name,
        )
        django_user.set_password(user.password)
        django_user.save()

        return DomainUser(
            id=django_user.id,
            name=django_user.name,
            cpf=django_user.cpf,
            password=django_user.password,
            created_at=timezone.localtime(django_user.created_at),
        )

    def get_by_cpf(self, cpf: str) -> DomainUser:
        # Busca o usuário no banco de dados pelo CPF
        try:
            DjangoUser = get_user_model()
            django_user = DjangoUser.objects.get(cpf=cpf)

            # Retorna o DomainUser
            return DomainUser(
                id=django_user.id,
                name=django_user.name,
                cpf=django_user.cpf,
                password=django_user.password,
                created_at=timezone.localtime(django_user.created_at),
            )
        except DjangoUser.DoesNotExist:
            return None
