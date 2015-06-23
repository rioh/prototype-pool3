import requests
import logging
import urllib
import json

from django.conf import settings


API_TYPES = {
    "events": settings.FDA_DRUG_API_EVENT_URL,
    "labels": settings.FDA_DRUG_API_LABEL_URL,
    "enforcements": settings.FDA_DRUG_API_ENFORCEMENT_URL}

BROWSE_TYPES = {
    "events": "patient.reaction.reactionmeddrapt",
    "labels": "openfda.brand_name",
    "enforcements": "state"}


class ApiClient(object):
    """
    API client code for consuming FDA opendata apis
    """
    logger = logging.getLogger(__name__)

    def __init__(self,  **kwargs):
        self.kwargs = kwargs
        self.api_limit = 100

    def search(self, query_string, api=None, filters=None):
        self.logger.debug("Searching for '%s'", query_string)
        filter_string = ""
        if filters:
            for key, value in filters.items():
                if filter_string != "":
                    filter_string += "&%s:%s" % (key, value)
                else:
                    filter_string += "+%s:%s" % (key, value)
        # TESTING
        if api == "events":
            filter_string = "&count=patient.drug.openfda.substance_name"
        data = {'q': query_string}
        if api is None:
            for t in API_TYPES.keys():
                data[t] = self.get_data(t, query_string, filter_string)
        else:
            data[api] = self.get_data(api, query_string, filter_string)

        return data

    def get_age_sex(self, api_type, param, filter_string):
        # grouping by male
        self.logger.debug("api_type: %s", api_type)
        male_filter = '+AND+patient.drug.openfda.substance_name:%s+AND+patient.patientsex:1' % filter_string
        url = '%s?search=%s%s' % (API_TYPES[api_type], urllib.quote(param), male_filter)
        self.logger.debug("url: %s", url)
        resp = requests.get(url)
        resp_json = resp.json()
        total_male = resp_json['meta']['results']['total']
        
        # grouping by female
        female_filter = '+AND+patient.drug.openfda.substance_name:%s+AND+patient.patientsex:2' % filter_string
        url = '%s?search=%s%s' % (API_TYPES[api_type], urllib.quote(param), female_filter)
        self.logger.debug("url: %s", url)
        resp = requests.get(url)
        resp_json = resp.json()
        total_female = resp_json['meta']['results']['total']
        return json.dumps([{
            "name": "Male",
            "data": [total_male]
        }, {
            "name": "Female",
            "data": [total_female]
        }]);

    def get_data(self, api_type, query_string, filter_string):

        results = None
        url = '%s?search=%s%s&limit=100' % (
            API_TYPES[api_type], urllib.quote(query_string), filter_string)
        self.logger.debug("url: %s", url)
        resp = requests.get(url)
        if resp.status_code == 200:
            resp_json = resp.json()
            results = resp_json.get('results')
            if resp_json['meta'].get('results'):
                total = resp_json['meta']['results']['total']
                self.logger.debug("%s results%", total)

                if total > self.api_limit:
                    # TODO: Cap this for now
                    if total > 500:
                        total = 500
                    for count in xrange(self.api_limit, total, self.api_limit):
                        self.logger.debug("getting the next %s results: %s / %s", self.api_limit, count, total)
                        url = "%s?search=%s%s&limit=100&skip=%d" % (
                            API_TYPES[api_type], query_string, filter_string, count)
                        self.logger.debug("url: %s", url)
                        results.append(requests.get(url).json().get('results'))
                else:
                    url = "%s?search=%s%s" % (
                        API_TYPES[api_type], query_string, filter_string)
                    self.logger.debug("url: %s", url)
                    results.append(requests.get(url).json().get('results'))
        else:
            self.logger.debug("got %s status code", resp.status_code)
        return results
        

    def browse(self, browse_type):
        data = requests.get("%s?count=%s.exact" % (API_TYPES.get(browse_type), BROWSE_TYPES.get(browse_type)))
        if data:
            results = data.json()
        return [{BROWSE_TYPES.get(browse_type): result.get('term')} for result in results.get('results')]
