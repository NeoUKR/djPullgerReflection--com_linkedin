from django.test import TestCase
from pullgerReflection.com_linkedin.tests.tools import unitOperationsR


class Test000Locations(TestCase):
    def test_000_add_search(self):
        unitOperationsR.add_location(self)
        new_search = unitOperationsR.add_search(self)

        # found_elements = models.ExecutionStackLinks.objects.filter(uuid_link=new_search.uuid).first()
        # found_elements.description = "Test"
        # found_elements.save()

        pass
