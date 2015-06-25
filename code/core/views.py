import logging

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

from .api_client import ApiClient


logger = logging.getLogger(__name__)


def homepage(request):
    return render(request, 'core/homepage.html')


def browse(request, browse_type):
    logger.debug("browsing %s", browse_type)
    client = ApiClient()
    data = {'browse_type': browse_type,
            'terms': client.browse(browse_type)}

    if browse_type == 'enforcements':
        return render(request, 'core/landing_enforcement_reports.html', data)
    elif browse_type == 'events':
        return render(request, 'core/landing_adverse_events.html', data)
    elif browse_type == 'labels':
        return render(request, 'core/landing_drug_labels.html', data)
    else:
        return render(request, 'core/landing_manufacturers.html', data)


def search_labels(request):
    client = ApiClient()
    query_term = request.GET.get('q')
    data = client.search_labels(query_term)
    data['q'] = query_term
    return render(request, 'core/details_drug_labels.html', data)


def search_label_events(request):
    client = ApiClient()
    query_string = request.GET.get('q')
    limit = request.GET.get('limit')
    skip = request.GET.get('skip')
    data = client.search_label_events(query_string, limit, skip)
    return HttpResponse(data, content_type='application/json')


def search_events(request):
    client = ApiClient()
    query_term = request.GET.get('q')
    data = client.search_events(query_term)
    data['q'] = query_term
    return render(request, 'core/details_adverse_events.html', data)


def search_enforcements(request):
    client = ApiClient()
    query_term = request.GET.get('q')
    data = client.search_enforcements(query_term)
    data['q'] = query_term
    return render(request, 'core/details_enforcement_reports.html', data)


# TODO -- this is pending
def search_manufacturers(request):
    client = ApiClient()
    query_term = request.GET.get('q')
    data = client.search_manufacturers(query_term)
    data['q'] = query_term
    return render(request, 'core/details_manufacturers.html', data)


def search_detail(request):
    results = {}
    if request.method == 'GET' and 'q' in request.GET:
        q = request.GET.get('q').strip()
        filter_string = request.GET.get('filter_string').strip()
        browse_type = request.GET.get('browse_type').strip()
        client = ApiClient()
        results = client.get_age_sex(browse_type, q, filter_string)
        return HttpResponse(results, content_type='application/json')
    return HttpResponseBadRequest()
