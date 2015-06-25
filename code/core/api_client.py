import requests
import logging
import urllib
import json
import operator

from django.conf import settings


API_TYPES = {
    "events": settings.FDA_DRUG_API_EVENT_URL,
    "labels": settings.FDA_DRUG_API_LABEL_URL,
    "enforcements": settings.FDA_DRUG_API_ENFORCEMENT_URL}


BROWSE_TYPES = {
    "events": "patient.reaction.reactionmeddrapt",
    "labels": "openfda.brand_name",
    "enforcements": "state",
    "manufacturers": {
        "events": "patient.drug.openfda.manufacturer_name",
        "labels": "openfda.manufacturer_name",
        "enforcements": "openfda.manufacturer_name"
    }
}


class ApiClient(object):
    """
    API client code for consuming FDA opendata apis
    """
    logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.api_limit = 100

    def browse(self, browse_type):
        if browse_type == 'manufacturers':
            return self._browse_manufacturers()

        results = {}
        data = requests.get("%s?count=%s.exact" % (API_TYPES.get(browse_type), BROWSE_TYPES.get(browse_type)))
        if data:
            results = data.json()

        return results.get('results')

    def _browse_manufacturers(self):
        """
        Get each of the manufacturer lists from the api sources. Return the combined json object.
        :return: list of combined manufacturer names and counts
        """
        data = {}

        # get the response from each of the queries
        for api_type, api_path in BROWSE_TYPES.get('manufacturers').items():
            self.logger.debug('Browsing for %s' % api_type)
            api_type_data = requests.get("%s?count=%s.exact" % (API_TYPES.get(api_type), api_path))

            if api_type_data:
                data[api_type] = api_type_data

        # if we got response(s), flatten them down
        if data:
            results = []
            for api_type, api_response in data.items():
                results += api_response.json().get('results')

            # and sort the list in number order
            if results:
                results = sorted(results, key=operator.itemgetter('count'), reverse=True)

        return results

    def search_labels(self, query_term):
        self.logger.debug("Searching for '%s'", query_term)
        data = {}

        # get general drug info
        data['labels'] = self.get_sub_data(
            "%s?search=openfda.brand_name:%s" % (
                API_TYPES['labels'], urllib.quote(query_term)), self.api_limit, 0)

        # get additional event info
        data['events'] = self.get_sub_data(
            "%s?search=patient.drug.medicinalproduct:%s" % (
                API_TYPES['events'], urllib.quote(query_term)), self.api_limit, 0)

        # get additional enforcement info
        data['enforcements'] = self.get_sub_data(
            "%s?search=product_description:%s" % (
                API_TYPES['enforcements'], urllib.quote(query_term)), self.api_limit, 0)
        return data

    def search_events(self, query_term):
        self.logger.debug("Searching for event '%s'", query_term)
        data = {}

        # get events counts
        count_string = "&count=patient.drug.openfda.substance_name"
        data['events_count'] = self.get_count_data(
            "%s?search=patient.reaction.reactionmeddrapt:%s%s" % (
                API_TYPES['events'], query_term, count_string))

        data['events'] = self.get_sub_data(
            "%s?search=patient.reaction.reactionmeddrapt:%s" % (
                API_TYPES['events'], query_term), self.api_limit, 0)
        return data

    def search_enforcements(self, query_term):
        self.logger.debug("Searching for enforcement '%s'", query_term)
        data = {}

        # get general enforcement info
        data['enforcements'] = self.get_sub_data(
            "%s?search=state:%s" % (
                API_TYPES['enforcements'], urllib.quote(query_term)), self.api_limit, 0)

        # get drug counts
        count_string = "&count=openfda.brand_name"
        data['drugs_count'] = self.get_count_data(
            "%s?search=state:%s%s" % (
                API_TYPES['enforcements'], query_term, count_string))
        return data

    def search_manufacturers(self, query_term):
        self.logger.debug("Searching for manufacturer '%s'", query_term)
        data = {}

        # get labels from this manufacturuer
        data['labels'] = self.get_sub_data(
            "%s?search=openfda.brand_name:%s" % (
                API_TYPES['labels'], urllib.quote(query_term)), self.api_limit, 0)

        # get additional event info
        data['events'] = self.get_sub_data(
            "%s?search=patient.drug.medicinalproduct:%s" % (
                API_TYPES['events'], urllib.quote(query_term)), self.api_limit, 0)

        # get additional enforcement info
        data['enforcements'] = self.get_sub_data(
            "%s?search=product_description:%s" % (
                API_TYPES['enforcements'], urllib.quote(query_term)), self.api_limit, 0)
        return data

        data = {}

        # get labels with this manufacturer

        # get adverse events with this manufacturer
        # https://api.fda.gov/drug/event.json?search=patient.drug.openfda.manufacturer_name:Mylan

        # get enforcement reports with this manufacturer
        # https://api.fda.gov/drug/enforcement.json?search=recalling_firm:Mylan




    def get_age_sex(self, api_type, param, filter_string):
        total_male = self.filter_patient(api_type, filter_string, param, 1)
        total_female = self.filter_patient(api_type, filter_string, param, 2)

        return json.dumps([{
            "name": "Male",
            "data": [total_male]
        }, {
            "name": "Female",
            "data": [total_female]
        }])

    def filter_patient(self, api_type, filter_string, param, identifier):
        filter = '+AND+patient.drug.openfda.substance_name:%s+AND+patient.patientsex:%s' % (filter_string, identifier)
        url = '%s?search=%s%s' % (API_TYPES[api_type], urllib.quote(param), filter)
        self.logger.debug("url: %s", url)
        resp = requests.get(url)
        resp_json = resp.json()
        return resp_json['meta']['results']['total']

    def get_sub_data(self, query_string, limit, skip):
        url = '%s&limit=%s&skip=%s' % (query_string, limit, skip)
        self.logger.debug("url: %s", url)
        resp = requests.get(url)
        if resp.status_code == 200:
            resp = requests.get(url).json().get('results')
            return resp
        self.logger.info('no results found for %s', query_string)
        return None

    def get_count_data(self, query_url):
        self.logger.debug("url: %s", query_url)
        resp = requests.get(query_url).json().get('results')
        return resp

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
