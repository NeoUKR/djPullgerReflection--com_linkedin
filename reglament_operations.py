'''
from datetime import datetime

def renewReglaments(InArg = None):
    from pyPullgerDomain.com.booking import port as bookingPort
    #import undetected_chromedriver.v2 as uc
    from . import metods
    
    allHotels = metods.getAllHotels()
    
    print("Debug #1");
    
    for curHotel in allHotels:
        print("Debug #2");
        country = bookingPort.LanguageWeb("ua")
        
        print("Debug #3");
        bookingMD = bookingPort.Phantom(curHotel.country)

        
        print("Debug #4");
        HotelCountry = bookingPort.Country(curHotel.country);
        hotelMD = bookingMD.getHotelByIDName(HotelCountry, curHotel.id_name)
        
        print("Debug #5");
        fetchHotelReview = hotelMD.fetchReviews();
        
        if fetchHotelReview != None:
            while fetchHotelReview.next():
                if metods.isReviewExist(fetchHotelReview.el.uuid_reviews) == False:
                    print("Debug #6 [" + fetchHotelReview.el.uuid_reviews + "] " + fetchHotelReview.el.userName);
                    metods.appendReview(curHotel.uuid, fetchHotelReview.el);
                else:
                    #Not need to search deeper
                    break;
                    
        bookingMD.close()
                    
def test2_operation(arg):
    
    print("step 0 reglament: " + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S %Z'));
    
    from pyPullgerDomain.com.booking import port as bookingPort

    print("step 1 reglament: " + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S %Z'));
    country = bookingPort.LanguageWeb("ua")
    
    print("step 2 reglament: " + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S %Z'));
    try:
        bookingMD = bookingPort.Phantom("uk")
    except:
        print("Error") 
    
    print("step 3 reglament: " + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S %Z'));
    hotelMD = bookingMD.getHotelByIDName(country, 'marmaros')
    
    fetchHotelReview = hotelMD.fetchReviews();
    
    if fetchHotelReview != None:
        while fetchHotelReview.next():
            print("ROW [" + str(fetchHotelReview.curentNum) + "]: ");
            print("\tb" + "UUID: " + str(fetchHotelReview.el.uuid_reviews));
            print("\tb" + "Name: " + str(fetchHotelReview.el.userName));
            print("\tb" + "Post date:"  + str(fetchHotelReview.el.post_date));
            print("\tb" + "Review bad: " + str(fetchHotelReview.el.review_bad));
            print("\tb" + "Review bad language: " + str(fetchHotelReview.el.review_bad_lang));
            print("\tb" + "Review good: " + str(fetchHotelReview.el.review_good));
            print("\tb" + "Review good language: " + str(fetchHotelReview.el.review_good_lang));
            
if __name__ == '__main__':
    test2_operation("");
'''