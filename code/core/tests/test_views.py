from mock import patch, MagicMock
from django.test import Client, TestCase


class BasicViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        resp = self.client.get('/', follow=True)
        self.assertEquals(resp.status_code, 200)

    @patch("core.api_client.ApiClient")
    def test_browse_events(self, mock_client):
        resp = self.client.get('/browse/events', follow=True)
        self.assertEquals(resp.status_code, 200)

    @patch("core.api_client.ApiClient")
    def test_browse_labels(self, mock_client):
        resp = self.client.get('/browse/labels', follow=True)
        self.assertEquals(resp.status_code, 200)

    @patch("core.api_client.ApiClient")
    def test_browse_enforcements(self, mock_client):
        resp = self.client.get('/browse/enforcements', follow=True)
        self.assertEquals(resp.status_code, 200)

    @patch("core.api_client.ApiClient")
    def test_search_labels(self, mock_client):
        resp = self.client.get('/search/labels?q=test', follow=True)
        self.assertEquals(resp.status_code, 200)

    @patch("core.api_client.ApiClient")
    def test_search_events(self, mock_client):
        resp = self.client.get('/search/events?q=test', follow=True)
        self.assertEquals(resp.status_code, 200)

    @patch("core.api_client.ApiClient")
    def test_search_enforcements(self, mock_client):
        resp = self.client.get('/search/enforcements?q=test', follow=True)
        self.assertEquals(resp.status_code, 200)

    # TODO: get around pickling error for mock objects
    @patch("core.api_client.ApiClient.get_age_sex")
    def xtest_search_detail(self, mock_client_method):
        mock_client_method.return_value = mock_response = MagicMock()
        mock_response.return_value = {}
        resp = self.client.get('/search_detail?q=test&browse_type=events&filter_string=aspirin', follow=True)
        self.assertEquals(resp.status_code, 200)
