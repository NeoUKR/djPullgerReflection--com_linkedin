from django.db.models import signals
from django.dispatch import receiver
from .models import people
from .models import companies
from .models import people_experience

@receiver(signals.pre_save, sender=people)
def add_people_uuid(sender, instance, **kwargs):
    import uuid

    if not instance.uuid:
        instance.uuid = str(uuid.uuid1())

@receiver(signals.pre_save, sender=companies)
def add_company_uuid(sender, instance, **kwargs):
    import uuid

    if not instance.uuid:
        instance.uuid = str(uuid.uuid1())


@receiver(signals.pre_save, sender=people_experience)
def add_people_experience_uuid(sender, instance, **kwargs):
    import uuid

    if not instance.uuid:
        instance.uuid = str(uuid.uuid1())