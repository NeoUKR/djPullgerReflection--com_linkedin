from pullgerReflection.com_linkedin.models import models_search


def add_people_search(locations: list, keywords: (list, str), **kwargs):
    if isinstance(keywords, list):
        keywords_prepared = ''.join(keywords)
    else:
        keywords_prepared = keywords
    return models_search.SearchRequests.add_search_request(
        scope="people",
        locations=locations,
        keywords=keywords_prepared
    )


def get_people_search_locations(search_request):
    return models_search.SearchRequestLocationsList.objects.get_search_locations(search_request)
