from pullgerReflection.com_linkedin import metods
from pullgerReflection.com_linkedin.models import people as People
from pullgerReflection.com_linkedin.models import companies as Companies_Model
from pullgerReflection.com_linkedin.models import people_experience as PeopleExperience
from pullgerReflection.com_linkedin.models import companies
from pyPullgerDomain.com.linkedin import port as linkedinPORT
from pullgerDomain.com.dnb import root as dnbROOT
from pullgerAccountManager.models import Accounts as Accounts_MODEL
import logging
import time

logging.basicConfig(filename="log22DEBUG.txt", level=logging.INFO, format="%(levelname)s %(asctime)s - %(name)s\n\t{process: %(process)s module: [%(module)s] line: %(lineno)d}\n\t%(relativeCreated)6d %(threadName)s\n\t\t%(message)s")

def createAccouts():

    accauntLIST = [
        {
            'login':'kkovalenko.sphere@outlook.com',
            'password':'bebb90cbf2',
        },
        {
            'login': 'ikovalenko.sphere@outlook.com',
            'password': 'Yxw6vgE7IVIMzvfKTZ5N',
            'limitPeopleCircle': 15,
            'limitPeopleMax': 120,
            'limitCompanyCircle': 20,
            'limitCompanyMax': 250,
        },
        {
            'login': 'developer.sphere@outlook.com',
            'password': 'nkValm76Ys8c6SSwk2Ci',
            'limitPeopleCircle': 15,
            'limitPeopleMax': 120,
            'limitCompanyCircle': 20,
            'limitCompanyMax': 250,
        },
        {
            'login': 'k.kovalenko@bukovel.com',
            'password': '137a8f2e37',
            'limitPeopleCircle': 15,
            'limitPeopleMax': 120,
            'limitCompanyCircle': 20,
            'limitCompanyMax': 250,
        },
        {
            'login': 'a.rosokhata@soft-industry.com',
            'password': 'arr192837',
            'limitPeopleCircle': 15,
            'limitPeopleMax': 120,
            'limitCompanyCircle': 20,
            'limitCompanyMax': 250,
        },
        {
            'login': 'y.com.julia@gmail.com',
            'password': 'zxc22linked.in',
            'limitPeopleCircle': 15,
            'limitPeopleMax': 120,
            'limitCompanyCircle': 20,
            'limitCompanyMax': 250,
        },
    ]

    for accauntDICT in accauntLIST:
        try:
            Accounts_MODEL.putAccount(**accauntDICT)
        except Exception as e:
            logging.critical(f'Cant add account. \n\t\tdata: {accauntDICT} \n\t\tdiscription: {e}')

    list = Accounts_MODEL.objects.getActualList()
    for curAccaunt in list:
        pass;
    pass;

'''
    shell -c "print('start');from djPullgerReflection.com_linkedin import tests;tests.createAccouts()"
'''

def testMultiAccountConnection():
    #Fill account stricrues
    listOfAccounts = []
    listOfConnections = []

    list = Accounts_MODEL.objects.getActualList()
    for curAccaunt in list:
        listOfAccounts.append(curAccaunt.uuid)
        listOfConnections.append(
            {
                'active':None,
                'connection':None,
                'object':curAccaunt,
            }
        )
    #Generate connections
    for curConnection in listOfConnections:
        curConnection['connection'] = linkedinPORT.Domain()
        try:
            AuthorizationResult = curConnection['connection'].authorization(curConnection['object'].login, curConnection['object'].password)
            if AuthorizationResult == True:
                curConnection['active'] = True;
            else:
                curConnection['active'] = False;
        except Exception as e:
            logging.error(f'Autorization error: {str(e)}')

    #Operation circle
    while True == True:
        AccesebleAccount = Accounts_MODEL.objects.getAccesebleAccount()
        if AccesebleAccount != None:
            try:
                AccesebleAccountIndex = listOfAccounts.index(AccesebleAccount.uuid)
            except:
                AccesebleAccountIndex = None

            if AccesebleAccountIndex != None:
                if listOfConnections[AccesebleAccountIndex]['active'] == True:
                    Connection = listOfConnections[AccesebleAccountIndex]['connection']
                    ConnectionObject = listOfConnections[AccesebleAccountIndex]['object']

                    try:
                        if ConnectionObject.getCountLimitOfPeople() < ConnectionObject.getLoadingLimitOfPeople():
                            CirclePeopleLimit = ConnectionObject.getCircleLimitOfPeople()
                            countLoaded = loadAllPerson(Connection, CirclePeopleLimit)
                            ConnectionObject.upCountOfPeople(countLoaded)
                        else:
                            ConnectionObject.renewAcessMoment()
                    except Exception as e:
                        logging.warning(str(e))
                        listOfConnections[AccesebleAccountIndex]['active'] = False

                    try:
                        if ConnectionObject.getCountLimitOfCompanies() < ConnectionObject.getLoadingLimitOfCompanies():
                            CircleCompanyLimit = ConnectionObject.getCircleLimitOfCompanies()
                            countloadedCompany = loadCompanies(Connection, CircleCompanyLimit)
                            ConnectionObject.upCountOfCompany(countloadedCompany)
                        else:
                            ConnectionObject.renewAcessMoment()

                    except Exception as e:
                        logging.warning(str(e))
                        listOfConnections[AccesebleAccountIndex]['active'] = False

                    ConnectionObject.renewAcessMoment()
                else:
                    ConnectionObject.renewAcessMoment()

        time.sleep(2)


    pass;

'''
shell -c "print('start');from djPullgerReflection.com_linkedin import tests;tests.testMultiAccountConnection()"
'''

def urlPersonNormalization():
    allPeoples = People.objects.getAllPersons();

    for curPeople in allPeoples:

        curPeople.cleaningURL()
        curPeople.save()

def dataPersonNormalization():
    allPeoples = People.objects.getAllPersons();

    for curPeople in allPeoples:
        if curPeople.nick == 'ildar0':
            test = 1

        normalizated = curPeople.normalization()
        if normalizated == True:
            curPeople.save()
'''
shell -c "print('start');from djPullgerReflection.com_linkedin import tests;tests.dataPersonNormalization()"
'''

def GetSearchResult():
    new = linkedinPORT.Domain();

    time.sleep(2)

    try:
        #AuthorizationResult = new.authorization('k.kovalenko@bukovel.com', '137a8f2e37')
        new.authorization('kkovalenko.sphere@outlook.com', 'bebb90cbf2')

        if new._authorizated == True:
            #.NET
            #Belarus
            #101728296 #Russia
            #104994045 #Moscow City, Russia
            #106686604 #StPetersburg City, Russia
            #Loaded #104359155 #Moscow, Russia
            #Loaded #103752778 #Yaroslavl’, Russia
            #Loaded #103574901 #Sverdlovsk, Russia
            #Loaded #105303715 #Krasnodar, Russia
            #Loaded #100020981 #Rostov, Russia
            #Loaded #102917175 #Tatarstan, Russia
            #Loaded #101777369 #Novosibirsk, Russia
            #Loaded #103249458 #Samara, Russia
            #Loaded #104523009 #Chelyabinsk, Russia
            #Loaded #100827052 #Nizhniy Novgorod, Russia
            #Loaded #102734387 #Bashkortostan, Russia
            #Loaded #107992632 #Novosibirsk, Novosibirsk, Russia
            #Loaded #107062619 #Perm, Russia
            #Loaded #100367933 #Yekaterinburg, Sverdlovsk, Russia
            #Loaded #100674497 #Krasnoyarsk, Russia
            #Loaded #102450862 #Rostov, Rostov, Russia
            #Loaded #101631519 #Kazan, Tatarstan, Russia

            test = 1
            # react
            #101705918 Belarus
            #101728296 #Russia
            #104994045 #Moscow City, Russia
            #106686604 #StPetersburg City, Russia
            #Loaded #104359155 #Moscow, Russia
            #103752778 #Yaroslavl’, Russia
            #103574901 #Sverdlovsk, Russia
            #105303715 #Krasnodar, Russia
            #100020981 #Rostov, Russia
            #102917175 #Tatarstan, Russia
            #101777369 #Novosibirsk, Russia
            #103249458 #Samara, Russia
            #104523009 #Chelyabinsk, Russia
            #100827052 #Nizhniy Novgorod, Russia
            #102734387 #Bashkortostan, Russia
            #107992632 #Novosibirsk, Novosibirsk, Russia
            #107062619 #Perm, Russia
            #100367933 #Yekaterinburg, Sverdlovsk, Russia
            #100674497 #Krasnoyarsk, Russia
            #102450862 #Rostov, Rostov, Russia
            #101631519 #Kazan, Tatarstan, Russia

            test = 1
            # django
            #Loaded partial #101705918 #Belarus
            #101728296 #Russia
            #104994045 #Moscow City, Russia
            #Loaded partial #106686604 #StPetersburg City, Russia
            #Loaded #104359155 #Moscow, Russia
            #103752778 #Yaroslavl’, Russia
            #103574901 #Sverdlovsk, Russia
            #105303715 #Krasnodar, Russia
            #100020981 #Rostov, Russia
            #102917175 #Tatarstan, Russia
            #101777369 #Novosibirsk, Russia
            #103249458 #Samara, Russia
            #104523009 #Chelyabinsk, Russia
            #100827052 #Nizhniy Novgorod, Russia
            #102734387 #Bashkortostan, Russia
            #107992632 #Novosibirsk, Novosibirsk, Russia
            #107062619 #Perm, Russia
            #100367933 #Yekaterinburg, Sverdlovsk, Russia
            #100674497 #Krasnoyarsk, Russia
            #102450862 #Rostov, Rostov, Russia
            #101631519 #Kazan, Tatarstan, Russia

            test = 1
            # java
            #101728296 #Russia
            #104994045 #Moscow City, Russia
            #106686604 #StPetersburg City, Russia
            #Loaded partial #104359155 #Moscow, Russia
            #103752778 #Yaroslavl’, Russia
            #103574901 #Sverdlovsk, Russia
            #105303715 #Krasnodar, Russia
            #100020981 #Rostov, Russia
            #102917175 #Tatarstan, Russia
            #101777369 #Novosibirsk, Russia
            #103249458 #Samara, Russia
            #104523009 #Chelyabinsk, Russia
            #100827052 #Nizhniy Novgorod, Russia
            #102734387 #Bashkortostan, Russia
            #107992632 #Novosibirsk, Novosibirsk, Russia
            #107062619 #Perm, Russia
            #100367933 #Yekaterinburg, Sverdlovsk, Russia
            #100674497 #Krasnoyarsk, Russia
            #102450862 #Rostov, Rostov, Russia
            #101631519 #Kazan, Tatarstan, Russia

            test = 1
            # C#
            #101728296 #Russia
            #104994045 #Moscow City, Russia
            #106686604 #StPetersburg City, Russia
            #104359155 #Moscow, Russia
            #103752778 #Yaroslavl’, Russia
            #103574901 #Sverdlovsk, Russia
            #105303715 #Krasnodar, Russia
            #100020981 #Rostov, Russia
            #102917175 #Tatarstan, Russia
            #101777369 #Novosibirsk, Russia
            #103249458 #Samara, Russia
            #104523009 #Chelyabinsk, Russia
            #100827052 #Nizhniy Novgorod, Russia
            #102734387 #Bashkortostan, Russia
            #107992632 #Novosibirsk, Novosibirsk, Russia
            #107062619 #Perm, Russia
            #100367933 #Yekaterinburg, Sverdlovsk, Russia
            #100674497 #Krasnoyarsk, Russia
            #102450862 #Rostov, Rostov, Russia
            #101631519 #Kazan, Tatarstan, Russia

            locations = [100674497]
            print(f'Loading locations: {locations[0]}')
            new.search('people', locations, "C#")

            countResults = new.getCountOfResults()

            if countResults < 12000:
                EndOfSearch = False

                while EndOfSearch == False:
                    time.sleep(4)
                    listOfPersons = new.getListOfPeoples()
                    print('List get: ' + str(len(listOfPersons)))

                    for elOfList in listOfPersons:
                        metods.addPeople(**elOfList);

                    if new.listOfPeopleNext() != True:
                        EndOfSearch = True;
                    # EndOfSearch = True;
            else:
                print(f'Persons to many!! {countResults}')
    except Exception as e:
        print(f'Error {str(e)}')
        new.close();

'''
shell -c "print('start');from djPullgerReflection.com_linkedin import tests;tests.GetSearchResult()"
'''


def loadAllPerson(InConnection = None, inLimit = None):

    if InConnection == None:
        domain = linkedinPORT.Domain();
        try:
            resultConnection = domain.authorization('kkovalenko.sphere@outlook.com', 'bebb90cbf2')
        except Exception as e:
            logging.critical(f'Authentification error: /n {str(e)}')
            resultConnection = None;
    else:
        domain = InConnection
        resultConnection = domain.connected

    if resultConnection == True:
        CardsArray = People.objects.getAllPersons(eq_date_loaded=None)
        logging.info(f'Processing people: not processed people: {len(CardsArray)}')
        limit = inLimit if inLimit != None else 20
        count = 0
        for CurCardPeople in CardsArray:
            count += 1

            if count > limit:
                break

            # new.getPerson(url = CurCardPeople.url)
            # new.getPerson(object=CurCardPeople)
            try:
                CurCardPeople.getDomain(domain)
            except Exception as e:
                if str(e) == 'incorrect page':
                    logging.info(f'Incorrect page for people uuid: [{CurCardPeople.uuid}] url: [{CurCardPeople.url}]')
                    continue
                else:
                    errorDiscription = str(e)
                    logging.warning(errorDiscription)
                    raise errorDiscription

            # CurCardPeople.DomainObject.squirrel.get(CurCardPeople.url + '/details/experience/')
            experieneceList = CurCardPeople.DomainObject.getListOfExperience()

            PeopleExperience.objects.delExperiences(uuid=CurCardPeople.uuid)
            errorsInLoop = False

            for curExperienece in experieneceList:
                if curExperienece['companyID'] != None or curExperienece['companyNICK'] != None:
                    newCompanyDict = {
                        "id" : curExperienece['companyID'],
                        "nick" : curExperienece['companyNICK'],
                        "name": curExperienece['companyName'],
                        "searcher": "NEO",
                        "url": curExperienece['companyURL']
                    }
                    newCompany = metods.addCompany(**newCompanyDict)

                    newPeopleExperienceDict = {
                        "job_discription": curExperienece['job_discription'],
                        "job_timing_type": curExperienece['job_timing_type']
                    }
                    resAddExperience = metods.addPeopleExperience(CurCardPeople, newCompany, **newPeopleExperienceDict)
                    if resAddExperience == None:
                        errorsInLoop = True;

            if errorsInLoop == False:
                metods.updateFullLoadDatePeople(people = CurCardPeople)

    if InConnection == None:
        domain.close();

    return count

'''
shell -c "print('start');from djPullgerReflection.com_linkedin import tests;tests.loadAllPerson()"
'''

def loadCompanies(inConnection = None, inLimit = None):

    i = 0
    limit = 100 if inLimit == None else inLimit

    criticalError = False

    if inConnection == None:
        rootDomain = linkedinPORT.Domain();
        connectionStatus = rootDomain.authorization('kkovalenko.sphere@outlook.com', 'bebb90cbf2')
    else:
        rootDomain = inConnection
        connectionStatus = rootDomain.connected

    # connectionStatus = rootDomain.connect()
    # connectionStatus = rootDomain.authorization('kkovalenko.sphere@outlook.com', 'bebb90cbf2')

    if connectionStatus:
        listCompanies = companies.objects.getList(eq_date_loaded = None)
        logging.info(f'Loading companies: find unloaded companies: {len(listCompanies)}')
        for curCompny in listCompanies:
            try:
                time.sleep(2)
                if curCompny.getDomain(rootDomain):
                    try:
                        curCompny.updateDATA()
                    except Exception as e:
                        logging.warning(f"""ERROR: cant update company
                            URL:{curCompny.url}     
                            UUID:{curCompny.uuid} NAME:{curCompny.name} ID:{curCompny.id} NICK:{curCompny.nick}. 
                            Error message:{str(e)}""")
                else:
                    splittedURL = list(filter(None, rootDomain.squirrel.current_url.split('/')))
                    if len(splittedURL) != 0 and splittedURL[-1] == 'unavailable':
                        curCompny.setUnavailable()
                        logging.warning(f'WARNING: Company unavalable UUID:{curCompny.uuid} NAME:{curCompny.name} ID:{curCompny.id} NICK:{curCompny.nick}')
                    else:
                        curCompny.setIncorrectLoad()
                        logging.warning(f'WARNING: Incorrect load company company UUID:{curCompny.uuid} NAME:{curCompny.name} ID:{curCompny.id} NICK:{curCompny.nick}')

                i += 1

                if i >= limit:
                    break
                else:
                    time.sleep(5)
            except BaseException as e:
                logging.warning(f'Error on load companies: [{str(e)}] company {curCompny.uuid} {curCompny.name} {curCompny.id}')
    else:
        # criticalError = True;
        raise Exception('Incorrect connection')

    if inConnection == None:
        rootDomain.close()

    logging.info(f'Load {i} companies.')
    # return criticalError;
    return i

'''
#
'''

def checkEqualHREF(firstHREF, secondHREF):
    listFirst = list(filter(None, firstHREF.split('/')))
    try: listFirst.remove('http:')
    except: pass
    try: listFirst.remove('https:')
    except: pass
    listFirstURL = listFirst[0].split('.')
    try: listFirstURL.remove('www')
    except: pass
    # del listFirstURL[-1]

    listSecond = list(filter(None, secondHREF.split('/')))
    try: listSecond.remove('http:')
    except: pass
    try: listSecond.remove('http2:')
    except: pass
    listSecondURL = listSecond[0].split('.')
    try: listSecondURL.remove('www')
    except: pass
    # del listSecondURL[-1]

    if len(listSecondURL) != 0:
        if listFirstURL == listSecondURL:
            return True
        else:            return False
    else:
        return False


def GetCorrectCompanyRevenue():
    dnbDOMAIN = dnbROOT.Root()

    listCompany = Companies_Model.objects.getSuitable()
    print(f'Find {len(listCompany)} to search Revenue')
    for curCompany in listCompany:
        try:
            faundedDNB_profile = None
            if curCompany.url_company != None:
                print(f'Search company with url: [{curCompany.url_company}]')

                searchResult = dnbDOMAIN.getSearch(curCompany.name)
                if len(searchResult.fetch) != 0:
                    companyFaund = False

                    for curSearchResult in searchResult.fetch:
                        dnbOrganization = curSearchResult.getOrganization()
                        if curCompany.url_company != None and dnbOrganization.website != None:
                            if checkEqualHREF(curCompany.url_company, dnbOrganization.website):
                                faundedDNB_profile = dnbOrganization
                                print(f'Find confirmety: {curCompany.url_company} revenue {dnbOrganization.revenue}')
                                break;
                else:
                    faundedDNB_profile = None
            else:
                faundedDNB_profile = None
        except Exception as e:
            print(f"Errors on Processing: {e}")

        try:
            curCompany.set_DBN_Prifile(faundedDNB_profile)
        except Exception as e:
            print(f"Error {str(e)}")

    dnbDOMAIN.squirrel.close()
'''
shell -c "print('start');from djPullgerReflection.com_linkedin import tests;tests.GetCorrectCompanyRevenue()"
'''

def PackageCompanyLoad():
    loadCompanies()
    GetCorrectCompanyRevenue()

'''
shell -c "print('start');from djPullgerReflection.com_linkedin import tests;tests.PackageCompanyLoad()"
'''

def CircleRun():
    for counter in range(40):
        loadAllPerson()
        time.sleep(900)
        criticalError = loadCompanies()
        if criticalError == True:
            print('Critical Error')
            break;
        time.sleep(900)
        # GetCorrectCompanyRevenue()
        # time.sleep(900)

'''
shell -c "print('start');from djPullgerReflection.com_linkedin import tests;tests.CircleRun()"
'''

def SearchRevenue():
    for counter in range(40):
        GetCorrectCompanyRevenue()

'''
shell -c "print('start');from djPullgerReflection.com_linkedin import tests;tests.SearchRevenue()"
'''


def loadCSV():
    from djPullgerReflection.com_linkedin import utils

    utils.loadCSV()

'''
shell -c "print('start');from djPullgerReflection.com_linkedin import tests;tests.loadCSV()"
'''




'''
from djPullgerReflection.com_linkedin.models import companies
ob = companies.objects.all()
cob = ob[3]
cob.domainConnection(user='kkovalenko.sphere@outlook.com', password='bebb90cbf2')

cob.reloadFunctions()
cob.updateDATA()

from pyPullgerFootPrint.com.linkedin.company import card
import importlib

importlib.reload(card)
card.getAboutData(squirrel=cob.domain.squirrel)

'''


'''
from djPullgerReflection.com_linkedin import tests
tests.colectCompanies()
'''


'''
from djPullgerReflection.com_linkedin.models import companies
companies().aa()


import importlib
importlib.reload(models_companies_functions)
'''

'''
from djPullgerReflection.com_linkedin.models import models_companies_functions

import importlib
importlib.reload(models_companies_functions)
models_companies_functions.aa()
'''

'''
from djPullgerReflection.com_linkedin import tests
rd = tests.bc()
import importlib
from pyPullgerDomain.com.linkedin.port import port_companies
CD = port_companies.CompanyDomain(root=rd)
CD.setCompany(id=2980493)
CD.goToAbout()


importlib.reload(port_companies)
CD = port_companies.CompanyDomain(root=rd)
CD.setCompany(id=27152955)
CD.goToAbout()

CD.goToAbout()

from pyPullgerFootPrint.com.linkedin.company import card
card.getID(squirrel=CD.squirrel)
card.getNick(squirrel=CD.squirrel)
card.getAbout(squirrel=CD.squirrel)


from pyPullgerFootPrint.com.linkedin.company import card
card.getAboutData(squirrel=CD.squirrel)
importlib.reload(card)
card.getLocations(squirrel=CD.squirrel)
'''
