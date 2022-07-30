'''
def testLanguage():
    from pyPullgerDomain.com.booking import port as bookingPort

    country = bookingPort.LanguageWeb("ua")
    return str(country.id)

def testGetCountry():
    from pyPullgerDomain.com.booking import port as bookingPort

    try:
        bookingMD = bookingPort.Phantom("uk")

        if bookingMD == None:
            respounce = str(bookingMD.languageWeb.id);
        else:
            respounce = 'Error';
    except:
        respounce = 'Responce:Error';

    return respounce;
'''