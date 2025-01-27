from django.contrib.auth import get_user_model
from django.utils import timezone
from core.entities.user import User


class DjangoUserRepository:
    def get_user_by_id(self, user_id: int) -> User:
        django_user = get_user_model().objects.get(id=user_id)
        created_at_brazil = timezone.localtime(django_user.created_at)
        return User(
            id=django_user.id,
            name=django_user.name,
            cpf=django_user.cpf,
            password=django_user.password,
            created_at=created_at_brazil,
        )

    def save(self, user: User) -> User:
        django_user = get_user_model()(
            name=user.name, cpf=user.cpf, password=user.password
        )
        django_user.save()
        return User(
            id=django_user.id,
            name=django_user.name,
            cpf=django_user.cpf,
            password=django_user.password,
            created_at=timezone.localtime(django_user.created_at),
        )
