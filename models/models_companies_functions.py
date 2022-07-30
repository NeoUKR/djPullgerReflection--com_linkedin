def aa():
    print('ok9')

def fillDATA(inClass):
    id = None
    card_type = None
    name = None
    locationNameGeneral = None
    countryISO = None
    overview = None
    industry = None
    company_size = None
    employee_linkedin = None
    url_company = None
    followers = None

    nick = None
    discription = None

    if type(inClass.domain.DATA) == dict:
        if 'ID' in inClass.domain.DATA:
            id = inClass.domain.DATA['ID']
        if 'LOCATIONS' in inClass.domain.DATA:
            LOCATIONS = inClass.domain.DATA['LOCATIONS']
            if type(LOCATIONS) == list:
                for curLocation in LOCATIONS:
                    countryISO = str(list(filter(None, curLocation.split(',')))[-1]).strip()
                    if len(countryISO) > 3:
                        countryISO = countryISO[-2:]
                    break
        if 'CARD_TYPE' in inClass.domain.DATA:
            card_type = inClass.domain.DATA['CARD_TYPE']
        if 'OVERVIEW' in inClass.domain.DATA:
            overview = inClass.domain.DATA['OVERVIEW']
        if 'INDUSTRY' in inClass.domain.DATA:
            industry = inClass.domain.DATA['INDUSTRY']
        if 'COMPANY_SIZE' in inClass.domain.DATA:
            company_size = inClass.domain.DATA['COMPANY_SIZE']
        if 'EMPLOYEE_LINKEDIN' in inClass.domain.DATA:
            employee_linkedin = inClass.domain.DATA['EMPLOYEE_LINKEDIN']
        if 'NAME' in inClass.domain.DATA:
            name = inClass.domain.DATA['NAME']
        if 'DISCRIPTION' in inClass.domain.DATA:
            discription = inClass.domain.DATA['DISCRIPTION']
        if 'LOCATION_NAME' in inClass.domain.DATA:
            locationNameGeneral = inClass.domain.DATA['LOCATION_NAME']
        if 'WEBSITE' in inClass.domain.DATA:
            url_company = inClass.domain.DATA['WEBSITE']
        if 'WEBSITE' in inClass.domain.DATA:
            url_company = inClass.domain.DATA['WEBSITE']
        if 'FOLLOWERS' in inClass.domain.DATA:
            followers = inClass.domain.DATA['FOLLOWERS']

        nick = inClass.domain.nick

    #Write the DATA
    if card_type != None and inClass.card_type == None:
        inClass.card_type = card_type
    if id != None and inClass.id == None:
        inClass.id = id
    if overview != None:
        inClass.overview = overview
    if countryISO != None:
        inClass.countryISO = countryISO
    if industry != None:
        inClass.industry = industry
    if company_size != None:
        inClass.company_size = company_size
    if employee_linkedin != None:
        inClass.employee_linkedin = employee_linkedin
    if nick != None:
        inClass.nick = nick
    if name != None:
        inClass.name = name
    if discription != None:
        inClass.discription = discription
    if locationNameGeneral != None:
        inClass.locationNameGeneral = locationNameGeneral
    if url_company != None:
        inClass.url_company = url_company
    if followers != None:
        inClass.followers = followers

