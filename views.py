'''
from django.http import HttpResponse
from djPullgerReflection.com_booking import metods


def domainGetLanguage(request):
    from . import test
    result = test.testLanguage();
    return HttpResponse("ok:" + str(result));

def domainGetCountry(request):
    from . import test
    result = test.testGetCountry();
    return HttpResponse("ok:" + str(result));

def isexist(request):
    #test = apps.get_app_config('reglament').verbose_name
    #reglament_app = apps.get_app_config('reglament');
    #test = reglament_app.test
    #reglament_app.scheduler.remove_job('my_job_id')
    #result = metods.isReviewExist("83975a3f-5de1-493a-a2b7-172f48d0fd3a")

    result = metods.isHotelExist("961ee5ba-e5a2-48ab-a28a-76caae54f57a")
    return HttpResponse("Hi. I am hire. result:" + str(result))

def isReviewExist(request):
    result = metods.isReviewExist("f50c85c85a35efdf")
    
    return HttpResponse("Hi. I am hire. result:" + str(result))

def renewReview(request):
    from . import reglament_operations
    
    #return HttpResponse("renewReview ok")
    reglament_operations.renewReglaments();
    return HttpResponse("Success")

def appendReview(request):
    result = metods.isHotelExist("83975a3f-5de1-493a-a2b7-172f48d0fd3a")
    reviewData = {};
    reviewData["uuid_reviews"] = "00000000-e5a2-48ab"; 
    reviewData["userName"] = "test user"; 
    reviewData["hotels_uuid"] = "eeb7dcd5-2edf-46c3-af62-8ebc512c0e83";
   
    metods.appendReview(reviewData);
    
    return HttpResponse("Renew reviews:" + str(reviewData["userName"]))

def appendOperation(request):
    from reglament import metods
    
    metods.appendOperation('test', '{"url":"http://podrobnosti.ua"}')
    
    return HttpResponse("Operation appended.")
'''