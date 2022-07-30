#from djPullgerReflection.com_linkedin import metods
from djPullgerReflection.com_linkedin.models import people
from djPullgerReflection.com_linkedin.models import companies
from djPullgerReflection.com_linkedin.models import people_experience

#Transfered
def getAllPersons(**kparams):
    if 'date_loaded' in kparams:
        return people.objects.filter(date_full_loaded=kparams['date_loaded'])
    elif 'lte_date_loaded' in kparams:
        return people.objects.filter(date_full_loaded__lte=kparams['lte_date_loaded'])
    else:
        return people.objects.all()

def isPeopleExist(peopleID):

    if type(peopleID) is int:
        if len(people.objects.filter(id = peopleID)[:1]) == 0:
            return False
        else:
            return True;
    else:
        return None;

#Transfered
def getPeopleByID(peopleID):
    res = people.objects.filter(id=peopleID)[:1]
    if len(res) == 1:
        return res[0]
    else:
        return None

#Transfered
def getPeopleByUUID(peopleUUID):
    res = people.objects.filter(uuid=peopleUUID)[:1]
    if len(res) == 1:
        return res[0]
    else:
        return None

def updateFullLoadDatePeople(**kParams):
    result = None
    elForeChange = None

    if 'people' in kParams:
        elForeChange = kParams['people']
    elif 'id' in kParams:
        elForeChange = getPeopleByUUID(kParams['id'])
    elif 'uuid' in kParams:
        elForeChange = getPeopleByID(kParams['uuid'])

    if elForeChange != None:
        from datetime import date
        elForeChange.date_full_loaded = date.today()
        elForeChange.save()
        result = True;

    return result

def addPeople(**dict):
    resultAdd = None;

    if 'id' in dict:
        IsPeopleExist = isPeopleExist(dict['id']);
        if IsPeopleExist != None:
            if IsPeopleExist == False:
                createRow = people();

                for key, value in dict.items():
                    if hasattr(createRow, key):
                        setattr(createRow, key, value)
                try:
                    createRow.save()
                    resultAdd = createRow
                except Exception as e:
                    print(e)
                    pass;
            else:
                resultAdd = getPeopleByID(dict['id'])


    return resultAdd;

def delPeople(inPeople):
    result = None

    if inPeople != None:
        inPeople.delete();
        result = True;

    return result;

def delPeopleByID(inID):
    return delPeople(getPeopleByID(inID))

def delPeopleByUUID(inUUID):
    return delPeople(getPeopleByUUID(inUUID))

# Company metods

def getAllCompanies(**kparams):
    if 'date_loaded' in kparams:
        return companies.objects.filter(date_full_loaded=kparams['date_loaded'])
    elif 'lte_date_loaded' in kparams:
        return companies.objects.filter(date_full_loaded__lte=kparams['lte_date_loaded'])
    else:
        return companies.objects.all()



def getCompanyByID(companyID):
    res = companies.objects.filter(id=companyID)
    if len(res) >= 1:
        if len(res) > 1:
            print(f'WARNING: dublicationg companies widh id {companyID}')
        return res[0]
    else:
        return None

def getCompanyByUUID(companyUUID):
    res = companies.objects.filter(uuid=companyUUID)
    if len(res) == 1:
        return res[0]
    else:
        return None

def getCompanyByNick(companyNICK):
    res = companies.objects.filter(nick=companyNICK)
    if len(res) >= 1:
        if len(res) > 1:
            print(f'WARNING: dublicationg companies widh nick {companyNICK}')
        return res[0]
    else:
        return None


def delCompanyByID(inID):
    result = None;
    findElement = getCompanyByID(inID)

    if findElement != None:
        findElement.delete();
        result = True;
    return result;

def delCompanyByUUID(inUUID):
    result = None;

    findElement = getCompanyByUUID(inUUID)

    if findElement != None:
        findElement.delete();
        result = True;
    return result;

def isConpanyExist(**kwargs):

    if 'id' in kwargs and kwargs['id'] != None:
        if type(kwargs['id']) is int:
            if len(companies.objects.filter(id = kwargs['id'])[:1]) == 0:
                return False
            else:
                return True;
        else:
            raise Exception('incorrect type id')
    elif 'nick' in kwargs and kwargs['nick'] != None:
        if type(kwargs['nick']) is str:
            if len(companies.objects.filter(nick = kwargs['nick'])[:1]) == 0:
                return False
            else:
                return True;
        else:
            raise Exception('incorrect nick')
    else:
        raise Exception('incorrect call')

def addCompany(**dict):
    if 'id' in dict and dict['id'] != None:
        company = getCompanyByID(dict['id'])
    elif 'nick' in dict and dict['nick'] != None:
        company = getCompanyByNick(dict['nick'])
    else:
        company = None

    if company == None:
        if isConpanyExist(**dict) == False:
            company = companies();

            for key, value in dict.items():
                if hasattr(company, key):
                    if (key != 'searcher' and value != None):

                        setattr(company, key, value)
            try:
                company.save()
            except Exception as e:
                raise Exception(f"Incorrect creating company: {str(e)}")
        else:
            raise Exception(f'Dublicate company: {str(dict)}')
    else:
        for key, value in dict.items():
            if hasattr(company, key):
                if getattr(company, key) == None:
                    setattr(company, key, value)

        try:
            company.save()
        except Exception as e:
            raise Exception(f"Incorrect creating company: {str(e)}")

    return company;

#Transfered
def _delExperiencesIntrnel(inPeople):
    result = True

    rowsExperiences = people_experience.objects.filter(people=inPeople.uuid)
    for rowExperiences in rowsExperiences:
        rowExperiences.delete()

    return result

#Transfered
def delExperiences(**kwards):
    result = None

    if 'uuid' in kwards:
        result = _delExperiencesIntrnel(getPeopleByUUID(kwards['uuid']))
    elif 'id' in kwards:
        result = _delExperiencesIntrnel(getPeopleByID(kwards['id']))
    elif 'people' in kwards:
        result = _delExperiencesIntrnel(kwards['people'])

    return result

def addPeopleExperience(people, company, **dict):
    resultAdd = None;

    createPeopleExperience = people_experience();

    for key, value in dict.items():
        if hasattr(createPeopleExperience, key):
            setattr(createPeopleExperience, key, value)
    try:
        createPeopleExperience.people = people
        createPeopleExperience.companies = company
        createPeopleExperience.save()
        resultAdd = createPeopleExperience
    except Exception as e:
        print(e)
        pass;

    return resultAdd;


'''
from djPullgerReflection.com_linkedin import metods
dd = { "id": 2323 }
res = metods.addPeople(**dd)

metods.getAllPersons()
metods.delPeopleByUUID('86b3c7a0-eefd-11ec-8ee2-d5c4034c4de5')
metods.delPeopleByID(2323)
'''


'''

def getAllHotels():
    return hotels.objects.all()
    
def appendReview(inHotelUUID, inData):
    
    createRow = reviews();
    createRow.hotels_uuid = inHotelUUID;
   
    if isinstance(inData, dict):
        useDict = True;
    else:
        useDict = False;
    
    for reviewsField in reviews._meta.get_fields():
        fieldName = reviewsField.name;
        
        if fieldName == "hotels_uuid":
            continue; 
        
        print("Field name: " + fieldName) 
        if useDict == True:
            if fieldName in inData:
                fieldDATA = inData[fieldName];
            else:
                continue; 
        else:
            if hasattr(inData , fieldName):
                fieldDATA = getattr(inData , fieldName)
                print("Field [" + fieldName+ "] = " + str(fieldDATA))
            else:
                print("No attribute: " + fieldName)
                continue;

        setattr(createRow, fieldName, fieldDATA);
    
    createRow.save();
     
    #appendReview
'''