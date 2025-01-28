from django.apps import AppConfig

class InfrastructureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'infrastructure'

    def ready(self):
        from django.apps import apps
        if not apps.is_installed('infrastructure.models'):
            from infrastructure.models import user_model
            self.models = {
                'customuser': user_model.CustomUser
            }