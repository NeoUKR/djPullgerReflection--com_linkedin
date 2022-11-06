from django.test import TestCase
from pullgerReflection.com_linkedin.tests.tools import unitOperationsR


class Test000Locations(TestCase):
    def test_000_add_location(self):
        uuid_new_people = unitOperationsR.add_location(self)
        pass
