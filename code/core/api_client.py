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

        # TODO: need to add pagination

        # get general drug info
        data['labels'] = self.clean_labels(self.get_sub_data(
            "%s?search=openfda.brand_name:\"%s\"" % (
                API_TYPES['labels'], urllib.quote(query_term)), self.api_limit, 0))

        # get additional event info
        data['events'] = self.clean_events(self.get_sub_data(
            "%s?search=patient.drug.medicinalproduct:\"%s\"" % (
                API_TYPES['events'], urllib.quote(query_term)), self.api_limit, 0))

        # get additional enforcement info
        data['enforcements'] = self.clean_enforcements(self.get_sub_data(
            "%s?search=product_description:\"%s\"" % (
                API_TYPES['enforcements'], urllib.quote(query_term)), self.api_limit, 0))

        return data

    def search_events(self, query_term):
        self.logger.debug("Searching for event '%s'", query_term)
        data = {}

        # get events counts
        count_string = "&count=patient.drug.openfda.substance_name"
        data['events_count'] = self.get_count_data(
            "%s?search=patient.reaction.reactionmeddrapt:\"%s\"%s" % (
                API_TYPES['events'], query_term, count_string))

        data['events'] = self.clean_events(self.get_sub_data(
            "%s?search=patient.reaction.reactionmeddrapt:\"%s\"" % (
                API_TYPES['events'], query_term), self.api_limit, 0))
        return data

    def search_enforcements(self, query_term):
        self.logger.debug("Searching for enforcement '%s'", query_term)
        data = {}

        # get general enforcement info
        data['enforcements'] = self.clean_enforcements(self.get_sub_data(
            "%s?search=state:\"%s\"" % (
                API_TYPES['enforcements'], urllib.quote(query_term)), self.api_limit, 0))

        # get drug counts
        count_string = "&count=openfda.brand_name"
        data['drugs_count'] = self.get_count_data(
            "%s?search=state:\"%s\"%s" % (
                API_TYPES['enforcements'], query_term, count_string))
        return data

    def search_manufacturers(self, query_term):
        self.logger.debug("Searching for manufacturer '%s'", query_term)
        data = {}

        # get labels from this manufacturer
        data['labels'] = self.clean_labels(self.get_sub_data(
            "%s?search=openfda.manufacturer_name:\"%s\"" % (
                API_TYPES['labels'], urllib.quote(query_term)), self.api_limit, 0))

        # get additional event info
        data['events'] = self.clean_events(self.get_sub_data(
            "%s?search=patient.drug.openfda.manufacturer_name:\"%s\"" % (
                API_TYPES['events'], urllib.quote(query_term)), self.api_limit, 0))

        # get additional enforcement info. we search for the name as manufacturer
        # Our original search was for manufacturer or recalling firm for this api, but the 'or'
        # query does not work.
        # Eg, https://api.fda.gov/drug/enforcement.json?search=openfda.manufacturer_name:
        # %22Pharmacia+and+Upjohn+Company%22+recalling_firm:%22Target%22 is broken

        data['enforcements'] = self.clean_enforcements(self.get_sub_data(
            "%s?search=openfda.manufacturer_name:\"%s\"" % (
                API_TYPES['enforcements'], urllib.quote(query_term)
                ), self.api_limit, 0))

        return data

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
        return []

    def get_count_data(self, query_url):
        self.logger.debug("url: %s", query_url)
        resp = requests.get(query_url).json().get('results')
        return resp

    def clean_labels(self, data):
        results = []
        for d in data:
            clean_data = {
                "id": d.get('id', {}),
                "brand_name": d.get('openfda', {}).get('brand_name'),
                "generic_name": d.get('openfda', {}).get('generic_name'),
                "description": d.get('openfda', {}).get('description'),
                "pharm_class_epc": d.get('openfda', {}).get('pharm_class_epc'),
                "pharm_class cs": d.get('openfda', {}).get('pharm_class_cs'),
                "route": d.get('openfda', {}).get('route'),
                "manufacturer": d.get('openfda', {}).get('manufacturer_name'),
                "do_not_use": d.get('openfda', {}).get('do_not_use'),
                "active_ingredient": d.get('active_ingredient'),
                "inactive_ingredient": d.get('inactive_ingredient'),
                "dosage_and_administration": d.get('dosage_and_administration'),
                "warnings": d.get('warnings'),
                "adverse_reactions": d.get('adverse_reactions'),
                "drug_interactions": d.get('drug_interactions'),
                "pharmacokinetics": d.get('pharmacokinetics'),
            }
            results.append(clean_data)
        return results

    def clean_events(self, data):
        results = []
        for d in data:
            safety_data = {
                "safety_report": d.get('safetyreportid'),
                "safety_report_version": d.get('safetyreportversion'),
                "receive_date": d.get('receivedate'),
                "receipt_date_format": d.get('receiptdateformat'),
                "seriousness": self.yes_or_no(d.get('seriousness')),
                "seriousness_details": ["congenital anomali: %s" % d.get("seriouscongenitalanomali"),
                                        "death: %s" % d.get("seriousnessdeath"),
                                        "disabling: %s" % d.get("seriousnessdisabling"),
                                        "hospitalization: %s" % d.get("seriousnesshospitalization"),
                                        "life threatening: %s" % d.get("seriousnesslifethreatening")],
                "duplicate_report_source": d.get('reportduplicate.duplicatesource'),
                "duplicate_report_number": d.get('reportduplicate.duplicatenumb'),
            }
            patient_data = {
                "patient_onset_age": "%s%s" % (d.get('patient.patientonsetstage', ""),
                                                d.get('patinetonsetageunit', "")),
                "patient_sex": self.male_or_female(d.get('patient.patientsex')),
                "patient_death_details": d.get('patient.patientdeath')
            }
            label_data = {
                "drug_administration_route": d.get('patient.drug.drugadministrationroute'),
                "actions_taken_with_drug": d.get('patient.drug.actiondrug'),
                "dosage": "%s%s" % (d.get('patient.drug.drugcumulativedosagenumb', ""),
                                    d.get('patient.drug.drugcumulativedosageunit', "")),
                "number_of_doses": d.get('patient.drug.drugstructuredosagenumb'),
                "reported_role_of_the_drug_in_the_adverse_event": d.get('patient.drug.drugcharacterization')
            }
            results.append({'safety_data': safety_data,
                            'patient_data': patient_data,
                            'label_data': label_data})
        return results

    def clean_enforcements(self, data):
        results = []
        for d in data:
            clean_data = {
                'event_id': d.get('event_id'),
                'status': d.get('status'),
                'city': d.get('city'),
                'state': d.get('state'),
                'recalling_firm': d.get('recalling_firm'),
                'reason_for_recall': d.get('reason_for_recall'),
                'manufacturer_name': d.get('openfda', {}).get('manufacturer_name'),
                'recall_initiation_date': d.get('recall_initiation_date'),
                'classification': d.get('classification'),
                'product_description': d.get('product_description'),
                'code_info': d.get('code_info'),
                'voluntary_mandated': d.get('voluntary_mandated'),
                'initial_firm_notification': d.get('initial_firm_notification'),
                'report_date': d.get('report_date'),
                'recall_initiation_date': d.get('recall_initiation_date'),
            }
            results.append(clean_data)
        return results

    def yes_or_no(self, value):
        if value == "1":
            return "Yes"
        elif value == "2":
            return "No"

    def male_or_female(self, value):
        if value == 1:
            return 'Male'
        elif value == 2:
            return 'Female'
        elif value == 0:
            return 'Unknown'
