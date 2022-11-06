from pullgerReflection.com_linkedin import models as com_linkedin_model
from pullgerInternalControl import pIC_pR


def add_people(**kwargs):
    model_object = com_linkedin_model.people

    newObjectInstance = model_object()

    for curField in model_object._meta.get_fields():
        if hasattr(curField, 'attname'):
            fieldName = getattr(curField, 'attname')
            value = kwargs.get(fieldName)
            if value is not None:
                setattr(newObjectInstance, fieldName, value)

    try:
        newObjectInstance.save()
        return newObjectInstance.uuid
    except BaseException as e:
        pIC_pR.Model.Error(
            msg="Can't save people object.",
            level=50,
            exception=e
        )


def get_people(**kwargs):
    if 'uuid' in kwargs:
        result = com_linkedin_model.people.objects.filter(uuid=kwargs['uuid'])
        if len(result) == 0:
            return None
        else:
            return result[0]
    else:
        raise pIC_pR.CORE.API(
            msg="Missing required argument [uuid].",
            level=30
        )