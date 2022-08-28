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

            def getMultisessionParameters(self):
                from pullgerAccountManager import structures
                from pullgerReflection.com_linkedin.ThreadOperations import people as ThreadOperations_people

                paramlist = {
                    'uuid_link': None,
                    'authorization': structures.authorizationsServers.linkedin(),
                    'loader': ThreadOperations_people.initialLoad(),
                    'taskFinalizer': None,
                }

                return paramlist


