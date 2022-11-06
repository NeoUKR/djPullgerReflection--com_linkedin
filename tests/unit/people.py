from django.test import TestCase
from pullgerReflection.com_linkedin.tests.tools import unitOperationsR


class Test000People(TestCase):
    def test_000_AddPeople(self):
        uuid_new_people = unitOperationsR.add_people(self)
        pass
