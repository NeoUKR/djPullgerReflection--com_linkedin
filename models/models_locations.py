import uuid

from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from pullgerInternalControl.pullgerReflection import Model as ModelExceptions
from pullgerInternalControl.pullgerReflection.Model.logging import logger


class LocationsManagers(models.Manager):

    def get_all(self):
        return self.all()

    def get_location(
            self,
            location: ("Locations", str, int)
    ) -> "Locations":

        location_prepared = None
        if isinstance(location, int) or isinstance(location, str):
            location_prepared = self.get_location_by_id(location)
        elif isinstance(location, Locations):
            location_prepared = location
        else:
            ModelExceptions.IncorrectType(
                msg="Incorrect type [id_location] most be int or str.",
                level=40
            )

        if isinstance(location_prepared, Locations) is False:
            ModelExceptions.General(
                msg=f"Cant find location {location} in DB",
                level=40
            )

        return location_prepared

    def get_location_by_id(self, id_location: (str, int)) -> "Locations":
        id_location_prepared = None
        if isinstance(id_location, int):
            id_location_prepared = id_location
        elif isinstance(id_location, str):
            id_location_prepared = int(id_location)
        else:
            ModelExceptions.IncorrectType(
                msg="Incorrect type [id_location] most be int or str.",
                level=40
            )

        result_query = self.filter(id_location=id_location_prepared)
        if len(result_query) == 0:
            return None
        else:
            if len(result_query) > 1:
                logger.warning(
                    msg=f"DB corrupt (several records with id [{str(id_location)}])"
                )
            return result_query.first()


class Locations(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    id_location = models.IntegerField(null=False)

    description = models.CharField(max_length=100, blank=False, null=False)

    # Registration change
    moment_create = models.DateField(auto_now_add=True, null=True)
    moment_update = models.DateField(auto_now=True, null=True)
    moment_sync = models.DateTimeField(null=True)
    # ---------------------------------------------------------------------
    objects = LocationsManagers()

    # ---------------------------------------------------------------------

    @staticmethod
    def add_locations(id_location: int = None, description: str = None, **kwargs):
        if id_location is not None:
            location_element = Locations.objects.get_location_by_id(id_location)

            if location_element is None:
                new_location = Locations()
                new_location.id_location = id_location
                if description is not None:
                    new_location.description = description
                else:
                    new_location.description = ""
                new_location.save()
            else:
                new_location = location_element

            return new_location
        else:
            ModelExceptions.IncorrectData(
                msg="No 'id_location' in request",
                level=30
            )


    def to_json(self):
        return(
            str({
                "uuid": str(self.uuid),
                "id_location": self.id_location,
                "description": self.description
            })
        )