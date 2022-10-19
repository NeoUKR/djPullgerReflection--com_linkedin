from django.apps import AppConfig
from pullgerInternalControl import pIC_pR


class com_linkedinConfig(AppConfig):
    name = 'pullgerReflection.com_linkedin'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import pullgerReflection.com_linkedin.signals  # noqa
        # Integration signals with TaskFlow
        try:
            import pullgerReflection.com_linkedin__TT.signals
        except BaseException as e:
            raise pIC_pR.TT.Integration(
                "Error on importing signals'",
                level=20,
                exception=e
            )
