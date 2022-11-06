import uuid

from django.db import models
from django.db.models import Q
from django.db.models import signals
from django.dispatch import receiver

from . import models_companies_functions
from pullgerDomain.com.linkedin import port
import importlib
from datetime import date
from pullgerInternalControl import pIC_pR
from pullgerInternalControl import pIC_pD

from pullgerDomain.com.linkedin import port
from pullgerInternalControl.pullgerReflection.Model.logging import logger


class CompaniesManager(models.Manager):
    testVar = None

    def is_exist(self, id_element: (str, int)) -> bool:
        if isinstance(id_element, int):
            identification = id_element
        elif isinstance(id_element, str):
            try:
                identification = int(id_element)
            except BaseException as e:
                pIC_pR.Model.IncorrectData(
                    msg=f"Incorrect type of id_people. [{str(e)}]",
                    level=30
                )
        else:
            pIC_pR.Model.IncorrectData(
                msg=f"Incorrect type of id_people. [{str(id_element)}]",
                level=30
            )

        filter_result = self.filter(id=identification)
        filter_result_count = len(filter_result)

        if filter_result_count == 0:
            return False
        else:
            if filter_result_count > 1:
                logger.warning(msg=f"Companies have id duplication [{id_element}]")
            return True

    def get_list(self, date_loaded=None, lte_date_loaded=None, eq_date_loaded=None):
        if date_loaded is not None:
            return self.filter(date_full_loaded=date_loaded)
        elif lte_date_loaded is not None:
            return self.filter(date_full_loaded__lte=lte_date_loaded)
        elif eq_date_loaded is not None:
            return self.filter(Q(date_full_loaded=eq_date_loaded))
        else:
            return self.all()

    @staticmethod
    def get_by_id(id_element: int):
        filter_result = Companies.objects.filter(id=id_element)
        filter_result_count = len(filter_result)

        if filter_result_count == 0:
            return None
        else:
            if filter_result_count > 1:
                logger.warning(msg=f"Companies have id duplication [{id_element}]")
            return filter_result.first()

    def get_by_uuid(self, uuid_element: str):
        return self.filter(uuid=uuid_element).first()

    def get_suitable(self):
        return self.filter(~Q(countryISO = 'RU'), ~Q(countryISO = 'UA'), ~Q(countryISO = None), Q(dnb_exist = None))

    def print_data(self):
        print(self)


CHOICES_CARD_TYPE = [('company', 'company'), ('school', 'school')]


class Companies(models.Model):
    # uuid = models.CharField(max_length=36, primary_key = True)
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    id = models.IntegerField(blank=False, null=True)
    nick = models.CharField(max_length=1000, null=True)
    name = models.CharField(max_length=500, null=True)

    card_type = models.CharField(choices = CHOICES_CARD_TYPE, max_length=100, null=True)

    description = models.CharField(max_length=300, null=True)
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

    # Revenue
    dnb_exist = models.BooleanField(blank=False, null=True)
    dnb_revenue = models.BigIntegerField(blank=False, null=True)
    dnb_profile = models.CharField(max_length=300, null=True)
    dnb_employee = models.IntegerField(blank=False, null=True)

    # Outsource company
    outsource_industry = models.BooleanField(blank=False, null=True)

    # Send to customer
    sendToCustomer = models.DateField(null=True)
    complies_parameters = models.BooleanField(blank=False, null=True)

    objects = CompaniesManager()
    domain = port.Domain

    def __next__(self):
        print("Next")

    @staticmethod
    def getCompanyByID(companyID):
        res = Companies.objects.filter(id=companyID)
        if len(res) >= 1:
            if len(res) > 1:
                print(f'WARNING: dublicationg companies widh id {companyID}')
            return res[0]
        else:
            return None
    @staticmethod
    def getCompanyByUUID(companyUUID):
        res = Companies.objects.filter(uuid=companyUUID)
        if len(res) == 1:
            return res[0]
        else:
            return None
    @staticmethod
    def getCompanyByNick(companyNICK):
        res = Companies.objects.filter(nick=companyNICK)
        if len(res) >= 1:
            if len(res) > 1:
                print(f'WARNING: dublicationg companies widh nick {companyNICK}')
            return res[0]
        else:
            return None
    @staticmethod
    def isConpanyExist(**kwargs):
        if 'id' in kwargs and kwargs['id'] != None:
            if type(kwargs['id']) is int:
                if len(Companies.objects.filter(id=kwargs['id'])[:1]) == 0:
                    return False
                else:
                    return True;
            else:
                raise Exception('incorrect type id')
        elif 'nick' in kwargs and kwargs['nick'] != None:
            if type(kwargs['nick']) is str:
                if len(Companies.objects.filter(nick=kwargs['nick'])[:1]) == 0:
                    return False
                else:
                    return True;
            else:
                raise Exception('incorrect nick')
        else:
            raise Exception('incorrect call')

    @staticmethod
    def add_company(**kwargs):
        if 'id' in kwargs and kwargs['id'] is not None:
            company = Companies.getCompanyByID(kwargs['id'])
        elif 'nick' in kwargs and kwargs['nick'] is not None:
            company = Companies.getCompanyByNick(kwargs['nick'])
        else:
            company = None

        if company == None:
            if Companies.isConpanyExist(**kwargs) is False:
                company = Companies();

                for key, value in kwargs.items():
                    if hasattr(company, key):
                        if key != 'searcher' and value is not None:
                            setattr(company, key, value)
                try:
                    company.save()
                except BaseException as e:
                    raise pIC_pR.Model.Error(
                        f"Incorrect creating company: {str(kwargs)}",
                        level=40,
                        exception=e
                    )
            else:
                raise pIC_pR.Model.Error(
                    f'Duplicate company: {str(kwargs)}',
                    level=40
                )
        else:
            for key, value in kwargs.items():
                if hasattr(company, key):
                    if getattr(company, key) is None:
                        setattr(company, key, value)
            try:
                company.save()
            except BaseException as e:
                raise pIC_pR.Model.Error(
                    f"Incorrect creating company: {str(kwargs)}",
                    level=40,
                    exception=e
                )

        return company;

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

    def get_domain(self, session):
        return session.domain.get_company(id_company=self.id)

        # result = None
        #
        # if self.domain == None:
        #     if 'root' in kwargs or domain != None:
        #         if domain != None:
        #             self.domain = port.CompanyDomain(root=domain)
        #         else:
        #             self.domain = port.CompanyDomain(root=kwargs['root'])
        #     elif 'squirrel' in kwargs:
        #         self.domain = port.CompanyDomain(squirrel=kwargs['squirrel'])
        #     else:
        #         self.domain = port.CompanyDomain()
        #
        # if self.domain != None:
        #     if self.domain.authorizated != True:
        #         if 'user' in kwargs and 'password' in kwargs:
        #             self.domain.authorization(kwargs['user'], kwargs['password'])
        #
        #     if self.domain.authorizated == True:
        #         if self.id != None:
        #             if self.domain.setCompany(id = self.id):
        #                 self.domain.pullDATA()
        #                 result = True
        #         elif  self.nick != None:
        #             if self.domain.setCompany(nick = self.nick):
        #                 self.domain.pullDATA()
        #                 result = True
        #
        #
        # return result

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

    def reloadFunctions(self):
        try:
            importlib.reload(models_companies_functions)
        except Exception as e:
            print(e)

    def getRevenueDNB(self):
        pass

    def sync(self=None, session=None, data=None):
        if self is None:
            if data is not None:
                self = Companies.save_data(data=data)
            else:
                pIC_pR.Model.Error(
                    msg=f"Empy variable DATA: [{str(e)}]",
                    level=50
                )
        else:
            if session is not None:
                pulled_data = self.pull_data(session=session)
                self.sync(data=pulled_data)
            elif data is not None:
                self.save_data(data=data)

        return self

    def save_data(self=None, data=None):
        if self is None:
            id_company = data.get('id')

            if id_company is not None:
                is_company_exist = Companies.objects.is_exist(id_company)

            if is_company_exist is False:
                self = Companies()
            else:
                self = Companies.objects.get_by_id(id_company)

        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        try:
            self.save()
        except Exception as e:
            pIC_pR.Model.Error(
                msg=f"Unexpected error on save People: [{str(e)}]"
            )

        return self

    def pull_data(self, session: object) -> list:
        company_domain = self.get_domain(session)
        if company_domain is None:
            raise pIC_pD.pages.General(
                msg="Error on page loading.",
                level=50
            )
        else:
            response = {
                     'meta': {
                     }
                }

            # models_companies_functions.fillDATA(self)
            # list_of_experience = company_domain.get_list_of_experience()
            #
            # for cur_experience in list_of_experience:
            #     response['people_experience'].append(cur_experience)

            return response

        # experience_list = self._object.DomainObject.get_list_of_experience()

        # import time
        #
        # session.domain.search(self.search_scope.lower(), self.get_locations_list(), self.keywords)
        # count_results = session.domain.get_count_of_results()
        #
        # response = {
        #     'meta': {
        #         'count_results': count_results
        #     },
        #     'elements': []
        # }
        #
        # EndOfSearch = False
        #
        # while EndOfSearch is False:
        #     time.sleep(4)
        #     listOfPersons = session.domain.getListOfPeoples()
        #     for elOfList in listOfPersons:
        #         response['elements'].append(elOfList)
        #
        #     if session.domain.listOfPeopleNext() is not True:
        #         EndOfSearch = True
        #
        # return response


companies = Companies

# @receiver(signals.pre_save, sender=Companies)
# def add_company_uuid(sender, instance, **kwargs):
#     import uuid
#
#     if not instance.uuid:
#         instance.uuid = str(uuid.uuid1())
