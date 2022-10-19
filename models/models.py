from datetime import date
from django.db import models
from django.db.models import Q

from .models_companies import companies
from pullgerDomain.com.linkedin import port as linkedinPORT
from pullgerFootPrint.com.linkedin import general as linkedinGENERAL
from pullgerInternalControl import pIC_pR


class PeopleManager(models.Manager):
    def getAllPersons(self, **kparams):
        if 'date_loaded' in kparams:
            return People.objects.filter(date_full_loaded=kparams['date_loaded'])
        elif 'lte_date_loaded' in kparams:
            return People.objects.filter(date_full_loaded__lte=kparams['lte_date_loaded'])
        elif 'ne_date_loaded' in kparams:
            return People.objects.filter(~Q(date_full_loaded=kparams['ne_date_loaded']))
        elif 'eq_date_loaded' in kparams:
            return People.objects.filter(Q(date_full_loaded=kparams['eq_date_loaded']))
        else:
            return People.objects.all()

    @staticmethod
    def getPeopleByUUID(peopleUUID):
        res = People.objects.filter(uuid=peopleUUID)[:1]
        if len(res) == 1:
            return res[0]
        else:
            return None

    @staticmethod
    def getPeopleByID(peopleID):
        res = People.objects.filter(id=peopleID)[:1]
        if len(res) == 1:
            return res[0]
        else:
            return None

class People(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True)
    id = models.IntegerField(blank=False, null=True)
    nick = models.CharField(max_length=150, null=True)

    first_name = models.CharField(max_length=150, null=True)
    second_name = models.CharField(max_length=150, null=True)
    full_name = models.CharField(max_length=300, null=True)

    url = models.CharField(max_length=300, null=True)
    discription = models.CharField(max_length=300, null=True)

    location = models.CharField(max_length=300, null=True)

    date_small_loaded = models.DateField(null=True)
    date_full_loaded = models.DateField(null=True)

    objects = PeopleManager()

    DomainObject = None

    def cleaningURL(self):
        self.url = linkedinPORT.PeopleSubject.getCleanedURL(self.url)

    def normalization(self):
        result = None
        if self.url != None:
            ## ==================================================
            urlClear = linkedinGENERAL.get_cleaned_url(self.url)
            if self.url != urlClear:
                self.url = urlClear
                result = True
            ## ==================================================
            ## ==================================================
            urlNICK = linkedinGENERAL.getNickFromURL(urlClear)
            # urlNICK = linkedinPORT.PeopleSubject.getNickFromURL(urlClear)
            if self.nick != urlNICK:
                self.nick = urlNICK
                result = True
            ## ==================================================
        return result

    def getDomain(self, linkedIN_DOMAIN = None):
        self.DomainObject = linkedIN_DOMAIN.getPerson(id = self.id, nick = self.nick)

    def updateFullLoadDatePeople(self):
        self.date_full_loaded = date.today()
        try:
            self.save()
        except BaseException as e:
            raise pIC_pR.Model.Error(
                'Not enough parameters. Need "object="',
                level=50,
                exception=e
            )


people = People


class People_ExperienceManager(models.Manager):
    @staticmethod
    def delExperiencesIntrnel(inPeople):
        rowsExperiences = people_experience.objects.filter(people=inPeople.uuid)
        for rowExperiences in rowsExperiences:
            rowExperiences.delete()

    # Transfered
    @staticmethod
    def delExperiences(**kwards):
        if 'uuid' in kwards:
            result = People_ExperienceManager._delExperiencesIntrnel(PeopleManager.getPeopleByUUID(kwards['uuid']))
        elif 'id' in kwards:
            result = People_ExperienceManager._delExperiencesIntrnel(PeopleManager.getPeopleByID(kwards['id']))
        elif 'people' in kwards:
            result = People_ExperienceManager._delExperiencesIntrnel(kwards['people'])

    @staticmethod
    def _delExperiencesIntrnel(inPeople):
        rowsExperiences = People_Experience.objects.filter(people=inPeople.uuid)
        for rowExperiences in rowsExperiences:
            rowExperiences.delete()

class People_Experience(models.Model):
    uuid = models.CharField(max_length=36, primary_key = True)
    people = models.ForeignKey(people, verbose_name = 'uuid_people', db_column='uuid_people', to_field = 'uuid', on_delete=models.CASCADE)
    companies = models.ForeignKey(companies, verbose_name = 'uuid_companies', db_column='uuid_companies', to_field = 'uuid', on_delete=models.CASCADE)
    job_discription = models.CharField(max_length=300, null=True)
    job_timing_type = models.CharField(max_length=50, null=True)
    date_small_loaded = models.DateField(null=True)

    objects = People_ExperienceManager()

    @staticmethod
    def addPeopleExperience(people, company, **dict):
        resultAdd = None;

        createPeopleExperience = People_Experience();

        for key, value in dict.items():
            if hasattr(createPeopleExperience, key):
                setattr(createPeopleExperience, key, value)
        try:
            createPeopleExperience.people = people
            createPeopleExperience.companies = company
            createPeopleExperience.save()
            resultAdd = createPeopleExperience
        except BaseException as e:
            raise pIC_pR.Model.Error(
                f"Incorrect creating company: {str(dict)}",
                exception=e
            )

        return resultAdd;


people_experience = People_Experience