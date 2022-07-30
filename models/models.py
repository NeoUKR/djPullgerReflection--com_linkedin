from django.db import models
from django.db.models import Q
from .models_companies import companies
from pyPullgerDomain.com.linkedin import port as linkedinPORT
from pyPullgerFootPrint.com.linkedin import general as linkedinGENERAL

class PeopleManager(models.Manager):
    def getAllPersons(self, **kparams):
        if 'date_loaded' in kparams:
            return people.objects.filter(date_full_loaded=kparams['date_loaded'])
        elif 'lte_date_loaded' in kparams:
            return people.objects.filter(date_full_loaded__lte=kparams['lte_date_loaded'])
        elif 'ne_date_loaded' in kparams:
            return people.objects.filter(~Q(date_full_loaded=kparams['ne_date_loaded']))
        elif 'eq_date_loaded' in kparams:
            return people.objects.filter(Q(date_full_loaded=kparams['eq_date_loaded']))
        else:
            return people.objects.all()
    @staticmethod
    def getPeopleByUUID(peopleUUID):
        res = people.objects.filter(uuid=peopleUUID)[:1]
        if len(res) == 1:
            return res[0]
        else:
            return None

    @staticmethod
    def getPeopleByID(peopleID):
        res = people.objects.filter(id=peopleID)[:1]
        if len(res) == 1:
            return res[0]
        else:
            return None



class people(models.Model):
    uuid = models.CharField(max_length=36, primary_key = True) 
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
            urlClear = linkedinGENERAL.getCleanedURL(self.url)
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

class People_Experience(models.Manager):
    @staticmethod
    def delExperiencesIntrnel(inPeople):
        result = True

        rowsExperiences = people_experience.objects.filter(people=inPeople.uuid)
        for rowExperiences in rowsExperiences:
            rowExperiences.delete()

        return result

    # Transfered
    @staticmethod
    def delExperiences(**kwards):
        result = None

        if 'uuid' in kwards:
            result = People_Experience.delExperiencesIntrnel(PeopleManager.getPeopleByUUID(kwards['uuid']))
        elif 'id' in kwards:
            result = People_Experience.delExperiencesIntrnel(PeopleManager.getPeopleByID(kwards['id']))
        elif 'people' in kwards:
            result = People_Experience.delExperiencesIntrnel(kwards['people'])

        return result


class people_experience(models.Model):
    uuid = models.CharField(max_length=36, primary_key = True)
    people = models.ForeignKey(people, verbose_name = 'uuid_people', db_column='uuid_people', to_field = 'uuid', on_delete=models.CASCADE)
    companies = models.ForeignKey(companies, verbose_name = 'uuid_companies', db_column='uuid_companies', to_field = 'uuid', on_delete=models.CASCADE)
    job_discription = models.CharField(max_length=300, null=True)
    job_timing_type = models.CharField(max_length=50, null=True)
    date_small_loaded = models.DateField(null=True)

    objects = People_Experience()