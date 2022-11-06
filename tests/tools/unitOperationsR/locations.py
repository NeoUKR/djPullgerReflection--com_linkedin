from pullgerReflection.com_linkedin import api
from pullgerReflection.com_linkedin.tests.tools import dataTemplatesR


def add_location(self):

    location_element_data_list = dataTemplatesR.location_data()
    for location_element_data in location_element_data_list:
        api.add_location(**location_element_data)

        new_location = api.get_location_by_id(**location_element_data)

        for (key, value) in location_element_data.items():
            self.assertEqual(getattr(new_location, key), value, "Incorrect compare DATA in new object")
