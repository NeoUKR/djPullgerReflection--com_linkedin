import uuid

from .models_people import People

from django.db import models
from django.db import transaction
from django.db.models import signals
from django.db.models import OuterRef, Subquery
from django.db.models import F
from django.dispatch import receiver

from .models_locations import Locations
from pullgerInternalControl.pullgerReflection import Model as ModelExceptions
from pullgerInternalControl.pullgerReflection.logging import logger
from pullgerDomain.com.linkedin import port


class SearchRequestsManager(models.Manager):
    def get_by_uuid(self, uuid_element: str):
        return self.filter(uuid=uuid_element).first()


class SearchRequests(models.Model):
    class SearchScopes(models.TextChoices):
        PEOPLE = 'PEOPLE', 'people'

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)

    search_scope = models.CharField(choices=SearchScopes.choices, max_length=100, blank=False, null=False)
    keywords = models.CharField(max_length=1000, blank=False, null=False)
    limited_respond = models.BooleanField(null=True)
    # Send to customer
    moment_create = models.DateTimeField(auto_now_add=True, null=True)
    moment_update = models.DateTimeField(auto_now=True, null=True)
    moment_sync = models.DateTimeField(null=True)

    updated = models.BooleanField(blank=False, null=True)

    objects = SearchRequestsManager()
    domain = port.Domain

    @property
    def db_table(self):
        return self._meta.db_table

    def get_results(self):
        return SearchRequestResult.objects.filter(search_request=self)

    @staticmethod
    def add_search_request(scope: str, locations: list, keywords: str):
        new_search_request = SearchRequests()
        new_search_request.keywords = keywords

        # check scope
        scope_prepared = scope.upper()
        if scope_prepared in SearchRequests.SearchScopes.values:
            new_search_request.search_scope = scope_prepared
        else:
            ModelExceptions.IncorrectData(
                msg=f"Scope {scope} not in list {str(SearchRequests.SearchScopes.values)}",
                level=40
            )

        locations_element_list = []
        if isinstance(locations, list):
            for cur_element in locations:
                location_element = Locations.objects.get_location(location=cur_element)

                if location_element is not None:
                    locations_element_list.append(location_element)
                else:
                    ModelExceptions.IncorrectData(
                        msg=f"Can't fill search location id {cur_element} in DB.",
                        level=30
                    )

        else:
            ModelExceptions.IncorrectType(
                msg="Incorrect type in locations_list",
                level=40
            )

        try:
            with transaction.atomic():
                new_search_request.save()

                for cur_locations_element in locations_element_list:
                    new_srl = SearchRequestLocationsList()
                    new_srl.search_request = new_search_request
                    new_srl.location = cur_locations_element
                    new_srl.save()
        except BaseException as e:
            ModelExceptions.General(
                msg="Incorrect type in locations_list",
                level=50,
                exception=e
            )

        return new_search_request

    def get_locations_list(self):
        result = SearchRequestLocationsList.objects.get_search_locations(self)
        response = []
        for cur_row in result:
            response.append(cur_row.id_location)

        return response

    def sync(self=None, data=None, session=None):
        if self is None:
            pass
        else:
            if data is not None:
                meta_data = data.get('meta')
                if meta_data is not None:
                    count_results = meta_data.get('count_results')
                    if count_results is not None:
                        try:
                            if int(count_results) > 1000:
                                self.limited_respond = True
                            else:
                                self.limited_respond = False
                            self.save()
                        except BaseException as e:
                            logger.warning(msg=f"Incorrect data in count_results. [{str(e)}]")
                    else:
                        logger.warning(msg=f"Incorrect meta data (no attribute [count_results])")
                else:
                    logger.warning(msg=f"Incorrect meta data (no attribute [meta])")

                from pullgerReflection.com_linkedin.models import models_people

                elements = data.get('elements')
                for cur_element in elements:
                    with transaction.atomic():
                        people_element = models_people.People.sync(data=cur_element)
                        SearchRequestResult.create_link(self, people_element)
            elif session is not None:
                pulled_data = self.pull_data(session)
                self.sync(data=pulled_data)
            else:
                ModelExceptions.IncorrectData(
                    msg="Incorrect function parameters.",
                    level=40
                )
        return self

    def pull_data(self, session):
        import time

        session.domain.search(self.search_scope.lower(), self.get_locations_list(), self.keywords)
        count_results = session.domain.get_count_of_results()

        response = {
            'meta': {
                'count_results': count_results
            },
            'elements': []
        }

        EndOfSearch = False

        while EndOfSearch is False:
            time.sleep(4)
            listOfPersons = session.domain.get_list_of_peoples()
            for elOfList in listOfPersons:
                response['elements'].append(elOfList)

            if session.domain.listOfPeopleNext() is not True:
                EndOfSearch = True

        return response


class SearchRequestLocationsListManager(models.Manager):

    def get_search_locations(self, search_request):
        result = self \
            .filter(search_request=search_request) \
            .select_related('location') \
            .annotate(id_location=F('location__id_location'))

        return result


class SearchRequestLocationsList(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    search_request = models.ForeignKey(
        SearchRequests,
        verbose_name='uuid_search_request',
        db_column='uuid_search_request',
        to_field='uuid',
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        Locations,
        verbose_name='uuid_locations',
        db_column='uuid_locations',
        to_field='uuid',
        on_delete=models.CASCADE
    )

    objects = SearchRequestLocationsListManager()


class SearchRequestResultManager(models.Manager):
    def is_link_exist(self, people):
        if len(self.filter(people=people)) > 0:
            return True
        else:
            return False


class SearchRequestResult(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    search_request = models.ForeignKey(
        SearchRequests,
        verbose_name='uuid_search_request',
        db_column='uuid_search_request',
        to_field='uuid',
        on_delete=models.CASCADE
    )
    people = models.ForeignKey(
        People,
        verbose_name='uuid_people',
        db_column='uuid_people',
        to_field='uuid',
        on_delete=models.CASCADE
    )

    objects = SearchRequestResultManager()

    @staticmethod
    def create_link(search_request, people):
        if SearchRequestResult.objects.is_link_exist(people) is False:
            new_search_request_result = SearchRequestResult()
            new_search_request_result.search_request = search_request
            new_search_request_result.people = people
            new_search_request_result.save()
