from contextlib import contextmanager
import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import RequestFactory

from selenium import webdriver
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait
from core.views import error400, error404, error500


# ----------------------------
# behavioral/functional tests based on user stories#
# ----------------------------

# SETTING TO MAKE SELENIUM WORK WITH FIREFOX ON MAC/LINUX
# export DISPLAY=:1


CATEGORIES = [{'name': 'Drug Names', 'detail': 'Drug Details', 'search': 'sovaldi'},
              {'name': 'Adverse Events', 'detail': 'Adverse Event Details', 'search': 'neutropenia'},
              {'name': 'Enforcement Reports', 'detail': 'Enforcement Report Details', 'search': 'UT'},
              {'name': 'Drug Manufacturers', 'detail': 'Manufacturer Details', 'search': 'Pfizer'}]


class ErrorTests(unittest.TestCase):
    """
    Site level error page tests
    """
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_400_on_bad_request(self):
        request = self.factory.get('/')
        response = error400(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'400 ERROR', response.content)
        self.assertIn(b'homepage', response.content)

    def test_get_404_on_not_found(self):
        request = self.factory.get('/')
        response = error404(request)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 ERROR', response.content)
        self.assertIn(b'homepage', response.content)

    def test_get_500_on_server_error(self):
        request = self.factory.get('/')
        response = error500(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'500 ERROR', response.content)
        self.assertIn(b'homepage', response.content)

class UserTests(StaticLiveServerTestCase):
    """
    Test that a user can navigate around the site
    """
    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.driver.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.driver, timeout).until(staleness_of(old_page))

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(3)

    def tearDown(self):
        self.driver.quit()

    def test_browse_navbar_categories(self):
        """
        Test that we can browse the site using the nav bar
        :return:
        """
        # 1a. I want to browse the top drug names by # of hits in the database
        # 1b. I want to browse the top adverse events by occurrence
        # 1c. I want to browse the enforcement reports by state
        # 1d. I want to browse the top manufacturers by # of hits in the db in alpha order
        for item in CATEGORIES:
            nav = item['name']
            self.driver.get(self.live_server_url)
            self.assertIn('Welcome to the FDA Drug Monitor', self.driver.find_element_by_tag_name('h1').text)

            # click the nav link on the nav bar
            drug_link = self.driver.find_element_by_link_text(nav)
            drug_link.click()
            self.assertIn(nav, self.driver.find_element_by_tag_name('h1').text)

            # there should be a list of the top items to browse
            drug_list = self.driver.find_elements_by_id('li')
            self.assertTrue('100', len(drug_list))

    # def test_search_categories(self):
    #     """
    #     Test that we can search the site using the different categories in the search bar
    #     :return:
    #     """
    #     # 2a. I want to search for a drug by name
    #     # 2b. I want to search for an adverse event by type
    #     # 2c. I want to search for a manufacturer by name
    #     # 2d. I want to search for enforcement reports by state
    #
    #     # click the search bar button without entering any values. Nothing should happen
    #     self.driver.get(self.live_server_url)
    #     self.assertIn('Welcome to the FDA Drug Monitor', self.driver.find_element_by_tag_name('h1').text)
    #
    #     search = self.driver.find_element_by_id('search-category')
    #     search.click()
    #     self.assertIn('Welcome to the FDA Drug Monitor', self.driver.find_element_by_tag_name('h1').text)
    #
    #     # test the search with categories and text
    #     for j, item in enumerate(CATEGORIES):
    #         self.driver.get(self.live_server_url)
    #         self.assertIn('Welcome to the FDA Drug Monitor', self.driver.find_element_by_tag_name('h1').text)
    #
    #         # select a search category and enter the keyword
    #         select = self.driver.find_element_by_id('select-category')
    #         options = select.find_elements_by_tag_name('option')
    #         options[j].click()
    #
    #         search_box = self.driver.find_element_by_xpath("//select[@id='select-category']/following-sibling::input")
    #         search_term = item['search']
    #         search_box.send_keys(search_term)
    #
    #         self.driver.find_element_by_id('search-category').click()
    #
    #         # we should go to the corresponding detail page and see our search term there
    #         self.assertIn(item['detail'], self.driver.find_element_by_tag_name('h1').text)
    #         self.assertIn(item['search'], self.driver.find_element_by_tag_name('h1').text)

# 3. I want to see adverse events for a specific drug

# 4. I want to see enforcement reports for a specific drug

# 5. I want to browse the top adverse events

# 6. I want to see reports for a given adverse events

# 7. I want to know the top drugs that have a given adverse event

# 8. I want to see the sex and age breakdown of the top drugs that have a given adverse event

# 9. I want to browse enforcement reports by state

# 10. I want to see enforcement report detail for a specific state

# 11. I want to see the specific drugs involved in a states' enforcement reports

# 12. I want to browse the top manufacturers

# 13. I want to see drugs made by a specific manufacturer

# 14. I want to see adverse events associated with a specific manufacturer

# 15. I wan to see enforcements associated with a specific manufacturer

