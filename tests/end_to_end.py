# from pullgerReflection.com_linkedin.tests import dataTemplate as dataTemplate_com_linkedin
from pullgerReflection.com_linkedin.tests import unit as unit_com_linkedin

from pullgerMultiSessionManager import api as pullgerMM__API
from rest_framework.test import APITestCase


class Test_001_FullCircle(APITestCase):
    def setUP(self):
        # TODO "Check the aviliability of all required modules: (UnitOperationsREST,)"
        # TODO "Clear sessions"
        pass

    # def test_001_people_load_head_browser(self):
    #     from pullgerReflection.com_linkedin__REST.tests import UnitOperations as UnitOperationsREST
    #
    #     UnitOperationsREST.setUpUnit(self)
    #     UnitOperationsREST.createPeople(self)
    #
    #     from pullgerAccountManager__REST.tests import UnitOperations as UnitOperationsAMRest
    #     UnitOperationsAMRest.addAccountForLinkedIN(self)
    #
    #     from pullgerMultiSessionManager__REST.tests import UnitOperations as UnitOperationsMM
    #     UnitOperationsMM.add_session_linkedin_standard(self)
    #     UnitOperationsMM.make_all_session_authorization(self)
    #
    #     UnitOperationsREST.send_all_task_to_processing(self)
    #
    #     UnitOperationsMM.execute_task_in_the_queue(self)
    #
    #     response = self.client.get("/pullgerR/com_linkedin/api/companies")
    #     self.assertEqual(response.status_code, 200, "Incorrect companies get data")
    #     self.assertNotEquals(response.data["data"]["count"], 0, "Incorrect list count")
    #
    #     pass
    #     #
    #     # pullgerMM__API.executeTask()
    #     # pullgerMM__API.executeTask()
    #     #
    #     # pullgerMM__API.executeFinalizer()
    #     # pass

    def test_000_people_load_head_browser(self):
        from pullgerReflection.com_linkedin__REST.tests import UnitOperations as UnitOperationsREST

        UnitOperationsREST.setUpUnit(self)
        UnitOperationsREST.createPeople(self)

        from pullgerAccountManager__REST.tests import UnitOperations as UnitOperationsAMRest
        UnitOperationsAMRest.addAccountForLinkedIN(self)

        from pullgerMultiSessionManager__REST.tests import UnitOperations as UnitOperationsMM
        UnitOperationsMM.add_session_linkedin_no_head(self)
        # UnitOperationsMM.add_session_linkedin_standard(self)
        UnitOperationsMM.make_all_session_authorization(self)

        UnitOperationsREST.send_all_task_to_processing(self)

        UnitOperationsMM.execute_task_in_the_queue(self)

        response = self.client.get("/pullgerR/com_linkedin/api/companies")
        self.assertEqual(response.status_code, 200, "Incorrect companies get data")
        self.assertNotEquals(response.data["data"]["count"], 0, "Incorrect list count")

        pass