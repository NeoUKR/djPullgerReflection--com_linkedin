from django.db import models
from django.db.models import Q
from . import models_companies_functions
from pyPullgerDomain.com.linkedin import port
import importlib
from datetime import date

class companiesManager(models.Manager):
    testVar = None

    def getList(self, **kparams):
        if 'date_loaded' in kparams:
            return companies.objects.filter(date_full_loaded=kparams['date_loaded'])
        elif 'lte_date_loaded' in kparams:
            return companies.objects.filter(date_full_loaded__lte=kparams['lte_date_loaded'])
        elif 'eq_date_loaded' in kparams:
            return companies.objects.filter(Q(date_full_loaded=kparams['eq_date_loaded']))
        else:
            return companies.objects.all()

    def getSuitable(self):
        return self.filter(~Q(countryISO = 'RU'), ~Q(countryISO = 'UA'), ~Q(countryISO = None), Q(dnb_exist = None))

    def printData(self):
        print(self)

CHOICES_CARD_TYPE = [('company', 'company') , ('school', 'school')]

# class CardChice():
#
#     def __init__(self):
#         for curChoice in CHOICES_CARD_TYPE:
#             setattr(self, curChoice[0], curChoice[1])

class companies(models.Model):
    uuid = models.CharField(max_length=36, primary_key = True)
    id = models.IntegerField(blank=False, null=True)
    nick = models.CharField(max_length=1000, null=True)
    name = models.CharField(max_length=500, null=True)

    card_type = models.CharField(choices = CHOICES_CARD_TYPE, max_length=100, null=True)

    discription = models.CharField(max_length=300, null=True)
    overview = models.TextField(null=True)

    account_closed = models.BooleanField(blank=False, null=True)
    incorrect_load = models.BooleanField(blank=False, null=True)

    url = models.CharField(max_length=300, null=True)
    url_company = models.CharField(max_length=300, null=True)

    industry = models.CharField(max_length=300, null=True)

    company_size = models.CharField(max_length=300, null=True)
    employee_linkedin = models.CharField(max_length=300, null=True)
    followers = models.IntegerField(blank=False, null=True)

    countryISO = models.CharField(max_length=3, null=True)
    location = models.CharField(max_length=300, null=True)
    locationNameGeneral = models.CharField(max_length=300, null=True)

    headquarter = models.CharField(max_length=300, null=True)
    founded = models.IntegerField(blank=False, null=True)

    searcher = models.CharField(max_length=100, null=True)

    date_small_loaded = models.DateField(null=True)
    date_full_loaded = models.DateField(null=True)

    #Revenue
    dnb_exist = models.BooleanField(blank=False, null=True)
    dnb_revenue = models.BigIntegerField(blank=False, null=True)
    dnb_profile = models.CharField(max_length=300, null=True)
    dnb_employee = models.IntegerField(blank=False, null=True)

    #Outsource company
    outsource_industry = models.BooleanField(blank=False, null=True)

    #Send to customer
    sendToCustomer = models.DateField(null=True)
    complies_parameters = models.BooleanField(blank=False, null=True)

    domain = None
    objects = companiesManager()

    def __next__(self):
        print("Next")

    def set_DBN_Prifile(self, object = None):
        if object == None:
            self.dnb_exist = False
            self.dnb_revenue = None
            self.dnb_profile = None
            self.save()
        else:
            self.dnb_exist = True;
            self.dnb_revenue = object.revenue
            self.dnb_profile = object.href
            self.save()


    # Variation of kwargs
    # root
    def getDomain(self, domain = None, **kwargs):
        result = None

        if self.domain == None:
            if 'root' in kwargs or domain != None:
                if domain != None:
                    self.domain = port.CompanyDomain(root=domain)
                else:
                    self.domain = port.CompanyDomain(root=kwargs['root'])
            elif 'squirrel' in kwargs:
                self.domain = port.CompanyDomain(squirrel=kwargs['squirrel'])
            else:
                self.domain = port.CompanyDomain()

        if self.domain != None:
            if self.domain.authorizated != True:
                if 'user' in kwargs and 'password' in kwargs:
                    self.domain.authorization(kwargs['user'], kwargs['password'])

            if self.domain.authorizated == True:
                if self.id != None:
                    if self.domain.setCompany(id = self.id):
                        self.domain.pullDATA()
                        result = True
                elif  self.nick != None:
                    if self.domain.setCompany(nick = self.nick):
                        self.domain.pullDATA()
                        result = True


        return result

    @classmethod
    def domainDisconection(cls):
        cls.domain == None

    def fillDATA(self):
        result = None
        try:
            models_companies_functions.fillDATA(self)
            result = True
        except Exception as e:
            print(e)
        return result

    def updateDATA(self):
        if self.fillDATA():
            self.date_full_loaded = date.today()
            if self.id != None:
                self.save()
            else:
                raise Exception("Can't save: in ID")

    def setUnavailable(self):
        self.date_full_loaded = date.today()
        self.account_closed = True;
        self.save()

    def setIncorrectLoad(self):
        self.date_full_loaded = date.today()
        self.incorrect_load = True;
        self.save()



    # def exec(self, inFunction):
    #     inFunction()

    def reloadFunctions(self):
        try:
            importlib.reload(models_companies_functions)
        except Exception as e:
            print(e)

    def getRevenueDNB(self):
        pass