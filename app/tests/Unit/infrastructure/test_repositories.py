import pytest
from django.utils import timezone
from infrastructure.repositories.django_user_repository import DjangoUserRepository
from core.entities.user import User

@pytest.mark.django_db
def test_save_user_with_timezone():
    repo = DjangoUserRepository()
    user = User(id=None, name="Bob", cpf="98765432100", password="senha_secreta")
    
    saved_user = repo.save(user)
    assert saved_user.created_at.tzinfo == timezone.get_current_timezone() 