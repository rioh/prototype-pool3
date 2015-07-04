import logging

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

from .api_client import ApiClient
from core.forms import ContactInformationForm
from core.models import ContactInformation


logger = logging.getLogger(__name__)


def homepage(request):
    return render(request, 'core/homepage.html')


def about(request):
    return render(request, 'core/about.html')


def accessibility(request):
    return render(request, 'core/accessibility.html')


# TODO -- create form and finish this method
# TODO -- strip html entities and sql injection check
def contact(request):
    data = {}
    if request.method == 'POST':
        contact_form = ContactInformationForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return HttpResponseRedirect('/')
        else:
            logger.debug('Form error: %s' % contact_form.errors)
            data['errors'] = contact_form.errors
            data['form'] = contact_form.data

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
    page = request.GET.get('page', '1')
    data = client.search_labels(query_term, int(page))
    data['q'] = query_term
    data['browse_type'] = 'labels'
    return render(request, 'core/details_drug_labels.html', data)


def search_label_events(request):
    client = ApiClient()
    query_term = request.GET.get('q')
    page = request.GET.get('page', '1')
    data = client.search_labels(query_term, int(page))
    return HttpResponse(data, content_type='application/json')


def search_events(request):
    client = ApiClient()
    query_term = request.GET.get('q')
    page = request.GET.get('page', '1')
    data = client.search_events(query_term, int(page))
    data['q'] = query_term
    data['browse_type'] = 'events'
    return render(request, 'core/details_adverse_events.html', data)


def search_enforcements(request):
    client = ApiClient()
    query_term = request.GET.get('q')
    page = request.GET.get('page', '1')
    data = client.search_enforcements(query_term, int(page))
    data['q'] = query_term
    data['browse_type'] = 'enforcements'
    return render(request, 'core/details_enforcement_reports.html', data)


# TODO -- add this method
def search_manufacturers(request):
    client = ApiClient()
    query_term = request.GET.get('q')
    page = request.GET.get('page', '1')
    data = client.search_manufacturers(query_term, int(page))
    data['q'] = query_term
    data['browse_type'] = 'manufacturers'
    return render(request, 'core/details_manufacturers.html', data)


def search_detail(request):
    results = {}
    if request.method == 'GET' and 'q' in request.GET:
        q = request.GET.get('q').strip()
        filter_string = request.GET.get('filter_string')
        browse_type = request.GET.get('browse_type')
        client = ApiClient()
        results = client.get_age_sex(browse_type, q, filter_string)
        return HttpResponse(results, content_type='application/json')
    return HttpResponseBadRequest()
