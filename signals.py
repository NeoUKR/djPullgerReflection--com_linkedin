from django.db.models import signals
from django.dispatch import receiver
from .models import People
from .models import Companies
from .models import people_experience


@receiver(signals.pre_save, sender=People)
def add_people_uuid(sender, instance, **kwargs):
    import uuid

    if not instance.uuid:
        instance.uuid = str(uuid.uuid1())

@receiver(signals.pre_save, sender=Companies)
def add_company_uuid(sender, instance, **kwargs):
    import uuid

    if not instance.uuid:
        instance.uuid = str(uuid.uuid1())


@receiver(signals.pre_save, sender=people_experience)
def add_people_experience_uuid(sender, instance, **kwargs):
    import uuid

    if not instance.uuid:
        instance.uuid = str(uuid.uuid1())