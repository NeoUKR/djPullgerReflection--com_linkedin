from django.apps import AppConfig
from pullgerReflection.exceptions import *

LOGGER_NAME = "pullger.Reflection.com_linkedin.apps"

class com_linkedinConfig(AppConfig):
    name = 'pullgerReflection.com_linkedin'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import pullgerReflection.com_linkedin.signals  # noqa
        # Integration signals with TaskFlow
        try:
            import pullgerReflection.com_linkedin__TT.signals
        except BaseException as e:
            raise excReflections_TT_Integration("Exception on connection library 'pullgerReflection.com_linkedin__TT.signals'", loggerName=LOGGER_NAME, level=20, parent=e)