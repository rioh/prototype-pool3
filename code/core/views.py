import logging

from django.shortcuts import render
from django.conf import settings
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
    return render(request, 'core/browse.html', data)


def search(request):
    if request.method == 'GET' and 'q' in request.GET:
        query_string = request.GET.get('q')
        browse_type = request.GET.get('browse_type')
        client = ApiClient()
        data = client.search(query_string, api=browse_type)
        return render(request, 'core/search_results.html', data)
    return HttpResponseBadRequest()

def result(request):
    return render(request, 'core/result.html')


def search_detail(request):
    results = {}
    if request.method == 'GET' and 'q' in request.GET:
        q = request.GET.get('q').strip()
        filter_string = request.GET.get('filter_string').strip()
        browse_type = request.GET.get('browse_type').strip()
        client = ApiClient()
        results = client.get_age_sex(browse_type, q, filter_string)
    return HttpResponse(results, content_type='application/json')
