from django.apps import AppConfig


class djPullgerReflection_com_linkedin_Config(AppConfig):
    name = 'djPullgerReflection.com_linkedin'

    def ready(self):
        import djPullgerReflection.com_linkedin.signals  # noqa
