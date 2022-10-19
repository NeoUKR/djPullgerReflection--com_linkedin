from abc import ABC

class TT_operation(ABC):
    pass

class Operations(object):
    @staticmethod
    def getOperationClassByName(inName):
        if inName == 'PEOPLE_INITIAL_LOAD':
            return Operations.PEOPLE.INITIAL_LOAD()

    class PEOPLE(ABC):
        class INITIAL_LOAD(object):
            name = 'PEOPLE_INITIAL_LOAD'

            def get_multi_session_parameters(self):
                from pullgerAccountManager import authorizationsServers
                from pullgerReflection.com_linkedin.ThreadOperations import people as ThreadOperations_people

                param_list = {
                    'uuid_link': None,
                    'authorization': authorizationsServers.linkedin.instances.general,
                    'loader': ThreadOperations_people.initialLoad(),
                    'taskFinalizer': None,
                }

                return param_list


