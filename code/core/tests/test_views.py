from mock import patch
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
    def test_search(self, mock_client):
        resp = self.client.get('/search/?q=test', follow=True)
        self.assertEquals(resp.status_code, 200)

    @patch("core.api_client.ApiClient")
    def test_search_bad_request(self, mock_client):
        resp = self.client.get('/search/', follow=True)
        self.assertEquals(resp.status_code, 400)

    @patch("core.api_client.ApiClient")
    def test_search_detail(self, mock_client):
        resp = self.client.get('/search_detail', follow=True)
        self.assertEquals(resp.status_code, 200)
