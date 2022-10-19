from pullgerInternalControl import pIC_pD
from .. import models as Reflection__com_linkedin_MODELS


class initialLoad(object):
    __slots__ = ('_object', '_domain')

    def __init__(self, **kwargs):
        pass

    def setObject(self, inObject):
        self._object = inObject

    def executeOnDomain(self, inDomain):
        self._object.getDomain(inDomain)
        try:
            experience_list = self._object.DomainObject.get_list_of_experience()
            # raise BaseException("test")
        except BaseException as e:
            raise pIC_pD.pages.General(
                msg="Error on 'get_list_of_experience'",
                level=50,
                exception=e
            )

        Reflection__com_linkedin_MODELS.People_Experience.objects.delExperiences(uuid=self._object.uuid)

        errorsInLoop = False

        for curExperience in experience_list:
            if curExperience['companyID'] is not None or curExperience['companyNICK'] is not None:
                newCompanyDict = {
                    "id": curExperience['companyID'],
                    "nick": curExperience['companyNICK'],
                    "name": curExperience['companyName'],
                    "searcher": "NEO",
                    "url": curExperience['companyURL']
                }
                newCompany = Reflection__com_linkedin_MODELS.Companies.addCompany(**newCompanyDict)

                newPeopleExperienceDict = {
                    "job_discription": curExperience['job_discription'],
                    "job_timing_type": curExperience['job_timing_type']
                }

                resAddExperience = Reflection__com_linkedin_MODELS.People_Experience.addPeopleExperience(self._object, newCompany, **newPeopleExperienceDict)
                if resAddExperience is None:
                    errorsInLoop = True

        if errorsInLoop is False:
            self._object.updateFullLoadDatePeople()
