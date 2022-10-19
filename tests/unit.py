from django.test import TestCase
from .. import api

class UnitOperations():
    @staticmethod
    def AddPeople(self):
        from .dataTemplate import person_DATA

        pDATA = person_DATA()
        uuidNewPeople = api.addPeople(**pDATA)
        self.assertEqual(len(uuidNewPeople), 36, "Incorrect uuid new People")
        createdElement = api.getPeople(uuid=uuidNewPeople)
        for (keyData, valueData) in pDATA.items():
            self.assertEqual(getattr(createdElement, keyData), valueData, f'Incorrect compare DATA on new object in [{keyData}] field: [{getattr(createdElement, keyData)}]<>[{valueData}]')

        return uuidNewPeople

class Test_000_People(TestCase):
    def test_000_AddPeople(self):
        uuidNewPeope = UnitOperations.AddPeople(self)

        pass

