from contextlib import contextmanager
import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import RequestFactory
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from core.views import error400, error404, error500


# ----------------------------
# behavioral/functional tests based on user stories#
# ----------------------------

# SETTING TO MAKE SELENIUM WORK WITH FIREFOX ON MAC/LINUX
# export DISPLAY=:1


CATEGORIES = [{'name': 'Drug Names', 'detail': 'Drug Details', 'search': 'sovaldi'},
              {'name': 'Adverse Events', 'detail': 'Adverse Event Details', 'search': 'purpura'},
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
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(3)

    def tearDown(self):
        self.driver.quit()

    def test_about_us(self):
        """
        Test that we can access about us page
        :return:
        """
        # I want to read information about the site
        self.driver.get('%s/about' % (self.live_server_url))
        self.assertIn('About', self.driver.find_element_by_tag_name('h1').text)

    def test_accessibility_page(self):
        """
        Test that we can access accessibility page
        :return:
        """
        # I want to read information about accesibility
        self.driver.get('%s/accessibility' % (self.live_server_url))
        self.assertIn('Accessibility', self.driver.find_element_by_tag_name('h1').text)

    def test_licensing_information(self):
        """
        Test that we can access licensing information
        :return:
        """
        # I want to read information about the site
        self.driver.get('%s/about' % (self.live_server_url))
        self.assertIn('Licensing', self.driver.find_element_by_tag_name('h2').text)

    def test_contact_form(self):
        """
        Test that we can submit a contact form
        :return:
        """
        # I want to submit a contact form to ask a question
        self.driver.get('%s/contact' % (self.live_server_url))
        self.assertIn('Contact', self.driver.find_element_by_tag_name('h1').text)

        # I try to submit the form without all the fields, but it doesn't go
        name = self.driver.find_element_by_id('contact-name')
        name.send_keys('test name')
        submit = self.driver.find_element_by_xpath("//form[@id='contact-form']//button")
        submit.click()
        self.assertIn('Contact', self.driver.find_element_by_tag_name('h1').text)

        # I enter all the fields but my email is bad
        name = self.driver.find_element_by_id('contact-name')
        name.send_keys('test name')
        email = self.driver.find_element_by_id('contact-email')
        email.send_keys('test@email')
        contact = self.driver.find_element_by_id('contact-comment')
        contact.send_keys('test comment')
        submit = self.driver.find_element_by_xpath("//form[@id='contact-form']//button")
        submit.click()
        self.assertIn('There was a problem',
                      self.driver.find_element_by_class_name('box-error').find_element_by_tag_name('h2').text)

        # I reenter all the fields correctly and submit the form
        email = self.driver.find_element_by_id('contact-email')
        email.send_keys('.com')
        submit = self.driver.find_element_by_xpath("//form[@id='contact-form']//button")
        submit.click()

        WebDriverWait(self.driver, 3).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), 'Welcome to the FDA Drug Monitor'))
        self.assertIn('Welcome to the FDA Drug Monitor', self.driver.find_element_by_tag_name('h1').text)

    def test_browse_navbar_categories(self):
        """
        Test that we can browse the site using the nav bar
        :return:
        """
        # I want to browse the top drug names by # of hits in the database
        # I want to browse the top adverse events by occurrence
        # I want to browse the enforcement reports by state
        # I want to browse the top manufacturers by # of hits in the db in alpha order

        for item in CATEGORIES:
            nav = item['name']
            self.driver.get(self.live_server_url)
            self.assertIn('Welcome to the FDA Drug Monitor', self.driver.find_element_by_tag_name('h1').text)

            # click the nav link on the nav bar
            drug_link = self.driver.find_element_by_link_text(nav)
            drug_link.click()
            self.assertIn(nav, self.driver.find_element_by_tag_name('h1').text)

            # there should be a list of the top items to browse
            browse_list = self.driver.find_element_by_class_name('fda-list-group').find_elements_by_id('li')
            self.assertTrue('100', len(browse_list))

            # click the first browse list item to go to its detail page
            browse_item = self.driver.find_element_by_xpath("//ul[@class='fda-list-group']/*[1]/a")
            browse_item.click()
            self.assertIn(item['detail'], self.driver.find_element_by_tag_name('h1').text)

    def test_browse_enforcement_by_map(self):
        """
        Test that we can select a state from enforcements and go to the detail page
        :return:
        """
        # I want to browse enforcments by states using a map. I will select UT.

        self.driver.get('%s/browse/enforcements' % (self.live_server_url))
        self.assertIn('Enforcement Reports', self.driver.find_element_by_tag_name('h1').text)

        state = self.driver.find_element_by_xpath(
            "//div[@id='map']//*[local-name()='svg']//*[local-name()='g'][@class='highcharts-series highcharts-tracker']//*[local-name()='path'][contains(@class, 'highcharts-name-ut')]")
        state.click()

        WebDriverWait(self.driver, 3).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), 'Enforcement Report Details'))
        self.assertIn('UT', self.driver.find_element_by_tag_name('h1').text)

    # TODO finish this test!
    def test_search_categories(self):
        """
        Test that we can search the site using the different categories in the search bar
        :return:
        """
        # I want to search for a drug by name
        # I want to search for an adverse event by type
        # I want to search for a manufacturer by name
        # I want to search for enforcement reports by state

        # click the search bar button without entering any values. Nothing should happen
        self.driver.get(self.live_server_url)
        self.assertIn('Welcome to the FDA Drug Monitor', self.driver.find_element_by_tag_name('h1').text)

        search = self.driver.find_element_by_id('search-category')
        search.click()
        self.assertIn('Welcome to the FDA Drug Monitor', self.driver.find_element_by_tag_name('h1').text)

        # test the search with categories and text
        for j, item in enumerate(CATEGORIES):
            search_term = item['search']
            self.driver.get(self.live_server_url)
            self.assertIn('Welcome to the FDA Drug Monitor', self.driver.find_element_by_tag_name('h1').text)

            # I select a search category and enter the keyword
            select = self.driver.find_element_by_id('select-category')
            options = select.find_elements_by_tag_name('option')
            options[j+1].click()

            search_box = self.driver.find_element_by_id('search-term')
            # switch the text input for state entry
            if item['name'] == 'Enforcement Reports':
                self.driver.implicitly_wait(3)
                search_box = self.driver.find_element_by_id('search-state')

            search_box.send_keys(search_term)
            self.driver.find_element_by_id('search-category').click()

            # we should go to the corresponding detail page
            WebDriverWait(self.driver, 3).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), item['detail']))
            self.assertIn(item['search'], self.driver.find_element_by_tag_name('h1').text)

    def test_drug_detail_page_tab1(self):
        """
        Test that the drug detail page has the tab and accordion items we expect
        :return:
        """
        # I want to see label details for a specific drug

        item = CATEGORIES[0]
        self.driver.get('%s/search/labels/?q=%s' % (self.live_server_url, item['search'] ))
        self.assertIn(item['detail'], self.driver.find_element_by_tag_name('h1').text)
        self.assertIn(item['search'], self.driver.find_element_by_tag_name('h1').text)

        # we should have three tabs
        self.assertEqual(3, len(self.driver.find_element_by_class_name('ui-tabs-nav').find_elements_by_tag_name('li')))
        self.driver.find_element_by_id('ui-id-1').click()

        # the details are hidden until i click the accordion
        labels_tab = self.driver.find_element_by_id('labels')
        self.assertIn(u'display: none;', labels_tab.find_element_by_id('labels_panel1').get_attribute('style'))
        details = labels_tab.find_elements_by_tag_name('h3')[0]
        details.click()
        self.assertIn(u'display: block;', labels_tab.find_element_by_id('labels_panel1').get_attribute('style'))

        # I can click 'more...' to see the longer items like adverse reactions
        adverse_row = self.driver.find_element_by_xpath(
            "//div[@id='labels_panel1']/table/tbody//th[./text()='Adverse reactions']/../td")
        text_div = adverse_row.find_element_by_tag_name('div')
        more_link = adverse_row.find_element_by_class_name('more')
        self.assertEqual(text_div.get_attribute('class'), u'text')
        more_link.click()
        self.assertEqual(text_div.get_attribute('class'), u'text expanded')

    def test_drug_detail_page_tab2(self):
        """
        Test that the drug detail page has the tab and accordion items we expect
        :return:
        """
        # I want to see adverse event details for a specific drug

        item = CATEGORIES[0]
        self.driver.get('%s/search/labels/?q=%s' % (self.live_server_url, item['search'],))
        self.assertIn(item['search'], self.driver.find_element_by_tag_name('h1').text)
        self.assertIn(item['detail'], self.driver.find_element_by_tag_name('h1').text)

        # we should have three tabs
        self.assertEqual(3, len(self.driver.find_element_by_class_name('ui-tabs-nav').find_elements_by_tag_name('li')))

        self.driver.find_element_by_id('ui-id-2').click()
        events_tab = self.driver.find_element_by_id('events')
        self.assertIn(u'display: none;', events_tab.find_element_by_id('events_panel1').get_attribute('style'))

        # the details are hidden until i click the first accordion
        details = events_tab.find_elements_by_tag_name('h3')[0]
        details.click()
        self.assertIn(u'display: block;', self.driver.find_element_by_id('events_panel1').get_attribute('style'))

        # I can click the accordion again to minimize it, then click the second accordion to expand it
        details.click()
        details_2 = events_tab.find_elements_by_tag_name('h3')[1]
        details_2.click()
        details_row = events_tab.find_element_by_id('events_panel2')
        self.assertIn(u'display: block;', details_row.get_attribute('style'))

        # There are three tables in the expanded data
        tables = details_row.find_elements_by_class_name('fda-table-default')
        self.assertEqual(3, len(tables))

    def test_drug_detail_page_tab3(self):
        """
        Test that the drug detail page has the tab and accordion items we expect
        (this test checks for 'No results found')
        :return:
        """
        # I want to see enforcement details for a specific drug

        item = CATEGORIES[0]
        self.driver.get('%s/search/labels/?q=%s' % (self.live_server_url, item['search'], ))
        self.assertIn(item['detail'], self.driver.find_element_by_tag_name('h1').text)
        self.assertIn(item['search'], self.driver.find_element_by_tag_name('h1').text)

        # we should have three tabs
        self.assertEqual(3, len(self.driver.find_element_by_class_name('ui-tabs-nav').find_elements_by_tag_name('li')))

        self.driver.find_element_by_id('ui-id-3').click()
        enforcements_tab = self.driver.find_element_by_id('enforcements')

        # there are no result for this tab
        self.assertIn(u'No results found', enforcements_tab.find_element_by_tag_name('p').text)

    def test_event_detail_page_tab1(self):
        """
        Test that the adverse event detail page has the tab and accordion items we expect
        :return:
        """
        # I want to see reports for a given adverse events

        item = CATEGORIES[1]
        self.driver.get('%s/search/events/?q=%s' % (self.live_server_url, item['search']))
        self.assertIn(item['detail'], self.driver.find_element_by_tag_name('h1').text)
        self.assertIn(item['search'], self.driver.find_element_by_tag_name('h1').text)

        # we should have two tabs
        self.assertEqual(2, len(self.driver.find_element_by_class_name('ui-tabs-nav').find_elements_by_tag_name('li')))

        # I want to see adverse events for a specific drug so i click that tab
        self.driver.find_element_by_id('ui-id-1').click()
        details_tab = self.driver.find_element_by_id('details')
        self.assertIn(u'display: none;', details_tab.find_element_by_id('events_panel1').get_attribute('style'))

        # the details are hidden until i click the first accordion
        details = details_tab.find_elements_by_tag_name('h3')[0]
        details.click()
        self.assertIn(u'display: block;', self.driver.find_element_by_id('events_panel1').get_attribute('style'))

        # I can click the accordion again to minimize it, then click the second accordion to expand it
        details.click()
        details_2 = details_tab.find_elements_by_tag_name('h3')[1]
        details_2.click()
        details_row = details_tab.find_element_by_id('events_panel2')
        self.assertIn(u'display: block;', details_row.get_attribute('style'))

        # There are three tables in the expanded data that contain report data
        tables = details_row.find_elements_by_class_name('fda-table-default')
        self.assertEqual(3, len(tables))

    def test_event_detail_page_tab2(self):
        """
        Test that the adverse event page has the tab and accordion items we expect
        :return:
        """
        # I want to see the top drugs that have a given adverse event
        # I want to see the sex and age breakdown of the top drugs that have a given adverse event

        item = CATEGORIES[1]
        self.driver.get('%s/search/events/?q=%s' % (self.live_server_url, item['search'], ))
        self.assertIn(item['detail'], self.driver.find_element_by_tag_name('h1').text)
        self.assertIn(item['search'], self.driver.find_element_by_tag_name('h1').text)

        # we should have two tabs
        self.assertEqual(2, len(self.driver.find_element_by_class_name('ui-tabs-nav').find_elements_by_tag_name('li')))

        # I want to see drugs with this adverse event, so i click that tab
        self.driver.find_element_by_id('ui-id-2').click()

        # I see a chart with drug information and I click and mouse over the first bar to get the count
        chart_bar = self.driver.find_element_by_xpath(
            "//div[@id='adverseChart']//*[local-name()='svg']//*[local-name()='g'][@class='highcharts-series highcharts-tracker']/*[local-name()='rect']")
        chart_bar.click()
        hover = ActionChains(self.driver).move_to_element(chart_bar)
        hover.perform()

        tool_tip = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='highcharts-tooltip']/span/div/span")))
        self.assertEqual('Count', tool_tip.text)

    def test_enforcement_detail_page_tab1(self):
        """
        Test that the enforcement detail page has the tab and accordion items we expect
        :return:
        """
        # I want to see enforcement report detail for a specific state

        item = CATEGORIES[2]
        self.driver.get('%s/search/enforcements/?q=%s' % (self.live_server_url, item['search']))
        self.assertIn(item['detail'], self.driver.find_element_by_tag_name('h1').text)
        self.assertIn(item['search'], self.driver.find_element_by_tag_name('h1').text)

        # we should have two tabs
        self.assertEqual(2, len(self.driver.find_element_by_class_name('ui-tabs-nav').find_elements_by_tag_name('li')))

        # I want to see reports for a specific drug so i click that tab
        self.driver.find_element_by_id('ui-id-1').click()
        details_tab = self.driver.find_element_by_id('details')
        self.assertIn(u'display: none;', details_tab.find_element_by_id('enforcements_panel1').get_attribute('style'))

        # the details are hidden until i click the first accordion
        details = details_tab.find_elements_by_tag_name('h3')[0]
        details.click()
        self.assertIn(u'display: block;', self.driver.find_element_by_id('enforcements_panel1').get_attribute('style'))

        # I can click the accordion again to minimize it, then click the second accordion to expand it
        details.click()
        details_2 = details_tab.find_elements_by_tag_name('h3')[1]
        details_2.click()
        details_row = details_tab.find_element_by_id('enforcements_panel2')
        self.assertIn(u'display: block;', details_row.get_attribute('style'))

        # There is one table in the expanded data that contain report data
        tables = details_row.find_elements_by_class_name('fda-table-default')
        self.assertEqual(1, len(tables))

    def test_enforcement_detail_page_tab2(self):
        """
        Test that the enforcement detail page has the tab and accordion items we expect
        :return:
        """
        # I want to see the specific drugs involved in a states' enforcement reports

        item = CATEGORIES[2]
        self.driver.get('%s/search/enforcements/?q=%s' % (self.live_server_url, item['search'], ))
        self.assertIn(item['detail'], self.driver.find_element_by_tag_name('h1').text)
        self.assertIn(item['search'], self.driver.find_element_by_tag_name('h1').text)

        # we should have two tabs
        self.assertEqual(2, len(self.driver.find_element_by_class_name('ui-tabs-nav').find_elements_by_tag_name('li')))

        # I want to see drugs with this adverse event, so i click that tab
        self.driver.find_element_by_id('ui-id-2').click()

        # I see a chart with drug information and I click the first drug to go to its detail page
        chart_bar = self.driver.find_element_by_xpath(
            "//div[@id='enforcementChart']//*[local-name()='svg']//*[local-name()='g'][@class='highcharts-series highcharts-tracker']/*[local-name()='rect']")
        chart_bar.click()

        WebDriverWait(self.driver, 3).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), 'Drug Details'))
        self.assertIn('Drug Details', self.driver.find_element_by_tag_name('h1').text)

    def test_manufacturer_detail_page_tab1(self):
        """
        Test that the drug detail page has the tab and accordion items we expect
        :return:
        """
        # 13. I want to see drugs made by a specific manufacturer

        item = CATEGORIES[3]
        self.driver.get('%s/search/manufacturers/?q=%s' % (self.live_server_url, item['search'] ))
        self.assertIn(item['detail'], self.driver.find_element_by_tag_name('h1').text)
        self.assertIn(item['search'], self.driver.find_element_by_tag_name('h1').text)

        # we should have three tabs
        self.assertEqual(3, len(self.driver.find_element_by_class_name('ui-tabs-nav').find_elements_by_tag_name('li')))
        self.driver.find_element_by_id('ui-id-1').click()

        # the details are hidden until i click the accordion
        labels_tab = self.driver.find_element_by_id('labels')
        self.assertIn(u'display: none;', labels_tab.find_element_by_id('labels_panel1').get_attribute('style'))
        details = labels_tab.find_elements_by_tag_name('h3')[0]
        details.click()
        self.assertIn(u'display: block;', labels_tab.find_element_by_id('labels_panel1').get_attribute('style'))

        # I can click 'more...' to see the longer items like adverse reactions
        adverse_row = self.driver.find_element_by_xpath(
            "//div[@id='labels_panel1']/table/tbody//th[./text()='Adverse reactions']/../td")
        text_div = adverse_row.find_element_by_tag_name('div')
        more_link = adverse_row.find_element_by_class_name('more')
        self.assertEqual(text_div.get_attribute('class'), u'text')
        more_link.click()
        self.assertEqual(text_div.get_attribute('class'), u'text expanded')

    def test_manufacturer_detail_page_tab2(self):
        """
        Test that the drug detail page has the tab and accordion items we expect
        :return:
        """
        # 14. I want to see adverse events associated with a specific manufacturer

        item = CATEGORIES[3]
        self.driver.get('%s/search/manufacturers/?q=%s' % (self.live_server_url, item['search'],))
        self.assertIn(item['detail'], self.driver.find_element_by_tag_name('h1').text)
        self.assertIn(item['search'], self.driver.find_element_by_tag_name('h1').text)

        # we should have three tabs
        self.assertEqual(3, len(self.driver.find_element_by_class_name('ui-tabs-nav').find_elements_by_tag_name('li')))

        self.driver.find_element_by_id('ui-id-2').click()
        events_tab = self.driver.find_element_by_id('events')
        self.assertIn(u'display: none;', events_tab.find_element_by_id('events_panel1').get_attribute('style'))

        # the details are hidden until i click the first accordion
        details = events_tab.find_elements_by_tag_name('h3')[0]
        details.click()
        self.assertIn(u'display: block;', self.driver.find_element_by_id('events_panel1').get_attribute('style'))

        # I can click the accordion again to minimize it, then click the second accordion to expand it
        details.click()
        details_2 = events_tab.find_elements_by_tag_name('h3')[1]
        details_2.click()
        details_row = events_tab.find_element_by_id('events_panel2')
        self.assertIn(u'display: block;', details_row.get_attribute('style'))

        # There are three tables in the expanded data
        tables = details_row.find_elements_by_class_name('fda-table-default')
        self.assertEqual(3, len(tables))

    def test_manufacturer_detail_page_tab3(self):
        """
        Test that the drug detail page has the tab and accordion items we expect
        (this test checks for 'No results found')
        :return:
        """
        # 15. I want to see enforcements associated with a specific manufacturer

        item = CATEGORIES[3]
        self.driver.get('%s/search/manufacturers/?q=%s' % (self.live_server_url, item['search'], ))
        self.assertIn(item['detail'], self.driver.find_element_by_tag_name('h1').text)
        self.assertIn(item['search'], self.driver.find_element_by_tag_name('h1').text)

        # we should have three tabs
        self.assertEqual(3, len(self.driver.find_element_by_class_name('ui-tabs-nav').find_elements_by_tag_name('li')))

        self.driver.find_element_by_id('ui-id-3').click()
        enforcements_tab = self.driver.find_element_by_id('enforcements')

        # the details are hidden until i click the first accordion
        details = enforcements_tab.find_elements_by_tag_name('h3')[0]
        details.click()
        self.assertIn(u'display: block;', self.driver.find_element_by_id('enforce_panel1').get_attribute('style'))

        # I can click the accordion again to minimize it, then click the second accordion to expand it
        details.click()
        details_2 = enforcements_tab.find_elements_by_tag_name('h3')[1]
        details_2.click()
        details_row = enforcements_tab.find_element_by_id('enforce_panel2')
        self.assertIn(u'display: block;', details_row.get_attribute('style'))

        # There is one table of data in the expanded accordion
        tables = details_row.find_elements_by_class_name('fda-table-default')
        self.assertEqual(1, len(tables))




