from functools import wraps

from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render

from .paginator import Paginator


def paginate(func):
    """
    Generates a paginated resultset
    """
    def inner(request, *args, **kwargs):
        try:
            page = request.GET.get('page', 1)
            per_page = settings.RESULTS_PER_PAGE
            paginator = Paginator(request)
            #paginator.paginate(page, per_page)
            results = func(request, paginator)
            pages = {'page': page, 'per_page': per_page, 'count': 10, 'pages': 1}
            pages['previous'] = ""
            pages['next'] = ""
            pages['first'] = ""
            pages['last'] = ""
            return render(request, results.get('page'), results.get('data'))
        except:
            return render(request, "", {})
    return wraps(func)(inner)
