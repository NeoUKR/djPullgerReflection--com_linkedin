from django.apps import AppConfig
from pullgerInternalControl import pIC_pR


class com_linkedinConfig(AppConfig):
    name = 'pullgerReflection.com_linkedin'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        pass
