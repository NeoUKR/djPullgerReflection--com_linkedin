from pullgerReflection.exceptions import *
from .. import models as Reflection__com_linkedin_MODELS
from pullgerExceptions import *

LOGGER_NAME = "pullger.Reflection.com_linkedin.ThreadOperations.people"

class initialLoad(object):
    __slots__ = ('_object' , '_domain')

    def __init__(self, **kwargs):
        pass
        # if 'object' in kwargs:
        #     self._object = kwargs['object']
        # else:
        #     raise excReflection_TT_IncorrectInputDATA('Not enough parameters. Need "object="', loggerName=LOGGER_NAME, level=50)
        #
        # if 'domain' in kwargs:
        #     self._domain = kwargs['domain']
        # else:
        #     raise excReflection_TT_IncorrectInputDATA('Not enough parameters. Need "domain="', loggerName=LOGGER_NAME, level=50)

    def setObject(self, inObject):
        self._object = inObject

    def executeOnDomain(self, inDomain):
        self._object.getDomain(inDomain)
        try:
            experieneceList = self._object.DomainObject.getListOfExperience()
        except BaseException as e:
            raise excDomain_Processing("Error on 'getListOfExperience'", level=50, exception=e)

        Reflection__com_linkedin_MODELS.People_Experience.objects.delExperiences(uuid=self._object.uuid)

        errorsInLoop = False

        for curExperienece in experieneceList:
            if curExperienece['companyID'] != None or curExperienece['companyNICK'] != None:
                newCompanyDict = {
                    "id": curExperienece['companyID'],
                    "nick": curExperienece['companyNICK'],
                    "name": curExperienece['companyName'],
                    "searcher": "NEO",
                    "url": curExperienece['companyURL']
                }
                newCompany = Reflection__com_linkedin_MODELS.Companies.addCompany(**newCompanyDict)

                newPeopleExperienceDict = {
                    "job_discription": curExperienece['job_discription'],
                    "job_timing_type": curExperienece['job_timing_type']
                }
                resAddExperience = Reflection__com_linkedin_MODELS.People_Experience.addPeopleExperience(self._object, newCompany, **newPeopleExperienceDict)
                if resAddExperience == None:
                    errorsInLoop = True;

        if errorsInLoop == False:
            self._object.updateFullLoadDatePeople()
