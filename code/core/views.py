import logging

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

from .api_client import ApiClient
from core.forms import ContactInformationForm


logger = logging.getLogger(__name__)


STATUS_CODES = {
    'HTTP_200_OK': 200,
    'HTTP_400_BAD_REQUEST': 400,
    'HTTP_404_NOT_FOUND': 404,
    'HTTP_405_METHOD_NOT_ALLOWED': 405,
    'HTTP_500_INTERNAL_SERVER_ERROR': 500
}

# custom error views
def error400(request):
    data = {'code': STATUS_CODES['HTTP_400_BAD_REQUEST'], 'detail': 'Bad request.'}
    return render(request, 'core/error.html', status=STATUS_CODES['HTTP_400_BAD_REQUEST'], context=data)


def error404(request):
    data = {'code': STATUS_CODES['HTTP_404_NOT_FOUND'], 'detail': 'The page you are looking for cannot be found.'}
    return render(request, 'core/error.html', status=STATUS_CODES['HTTP_404_NOT_FOUND'], context=data)


def error500(request):
    data = {'code': STATUS_CODES['HTTP_500_INTERNAL_SERVER_ERROR'], 'detail': 'Internal server error. Please try your request again.'}
    return render(request, 'core/error.html', status=STATUS_CODES['HTTP_500_INTERNAL_SERVER_ERROR'], context=data)


# site views
def homepage(request):
    return render(request, 'core/homepage.html')


def about(request):
    return render(request, 'core/about.html')


def accessibility(request):
    return render(request, 'core/accessibility.html')


def contact(request):
    data = {}
    if request.method == 'POST':
        contact_form = ContactInformationForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return HttpResponseRedirect('/')
        else:
            # pass the errors and data back to the form; the template will escape html as needed
            data['errors'] = contact_form.errors
            data['formdata'] = request.POST

    return render(request, 'core/contact.html', data)


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
    data['browse_type'] = 'labels'
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
    data['browse_type'] = 'events'
    return render(request, 'core/details_adverse_events.html', data)


def search_enforcements(request):
    client = ApiClient()
    query_term = request.GET.get('q')
    data = client.search_enforcements(query_term)
    data['q'] = query_term
    data['browse_type'] = 'enforcements'
    return render(request, 'core/details_enforcement_reports.html', data)


# TODO -- add this method
def search_manufacturers(request):
    client = ApiClient()
    query_term = request.GET.get('q')
    data = client.search_manufacturers(query_term)
    data['q'] = query_term
    data['browse_type'] = 'manufacturers'
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
