from pullgerReflection.com_linkedin.models import models_locations


def add_location(id_location: int, description: str, **kwargs):
    return models_locations.Locations.add_locations(id_location=id_location, description=description)


def get_location_by_id(id_location: int, **kwargs):
    return models_locations.Locations.objects.get_location_by_id(id_location=id_location)
