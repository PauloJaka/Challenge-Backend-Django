from django.test import TestCase
from django.utils import timezone
from domain.entities.user import User
from infrastructure.repositories.django_user_repository import DjangoUserRepository

class TestDjangoUserRepository(TestCase):
    def setUp(self):
        self.repository = DjangoUserRepository()
    
    def test_save_user_with_timezone(self):
        # Arrange
        user = User(
            id=None,
            name="Bob",
            cpf="98765432100",
            password="senha123",
            created_at=None
        )
        
        # Act
        saved_user = self.repository.save(user)
        
        # Assert
        self.assertIsNotNone(saved_user.id)
        self.assertEqual(saved_user.name, "Bob")
        self.assertEqual(saved_user.cpf, "98765432100")
        self.assertIsNotNone(saved_user.created_at)