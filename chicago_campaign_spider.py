from selenium import webdriver
import logging

logging.basicConfig(filename='campaign_spider.log',level=logging.DEBUG)

class CampaignSpider(object):
    name = 'CampaignSpider'
    allowed_domains = ['http://www.chicagoelections.com']
    start_urls = ['http://www.chicagoelections.com/en/election3.asp']

    def __init__(self, election, position):
        self.driver = webdriver.Firefox()
        self.election = election
        self.position = position
        self.elections_visited = []

    def parse_all_election_data(self):
        self.driver.get('http://www.chicagoelections.com/en/election3.asp')

        main_page_options = self.get_dropdown_options('//select[@name="D3"]')

        self.main_page_options = [option.text for option in main_page_options]
        print self.main_page_options

        for option_text in self.main_page_options:
            if self.election in option_text.lower() and option_text not in self.elections_visited:
                campaign = str(option_text)
                self.elections_visited.append(campaign)
                text_with_whitespace = '{message: <{width}}'.format(message=option_text, width=50)
                option = self.driver.find_element_by_xpath('//select[@name="D3"]/option[@value="%s"]' % text_with_whitespace)
                option.click()
                logging.info("Clicking on %s" % campaign)
                self.click_submit('//input[@type="submit"]')
                self.parse_campaign_election_data(campaign)
                print "we finished %s" % campaign
                self.driver.get('http://www.chicagoelections.com/en/election3.asp')

    def parse_campaign_election_data(self, campaign):
        try:
            current_campaign_options = self.get_dropdown_options('//select[@name="D3"]')
            for option in current_campaign_options:
                if option.text.lower() == self.position:
                    option.click()
                    break
            self.click_submit('//input[@value="  View The Results   "]')

            data = []
            counter = 0
            for tr in self.get_tablerows('//table[@width="100%"]//tr'):
                tds=tr.find_elements_by_tag_name('td')
                if tds:
                    counter += 1
                    print "%s adding record %s" % (campaign, counter)
                    data.append([td.text for td in tds])

        except:
            logging.debug("failed to get campaign data for %s" % campaign)
            pass

        return data

    def get_dropdown_options(self, xpath):
        main_dropdown = self.driver.find_element_by_xpath(xpath)
        return main_dropdown.find_elements_by_tag_name('option')

    def get_tablerows(self, xpath):
        return self.driver.find_elements_by_xpath(xpath)

    def click_submit(self, xpath):
        submit = self.driver.find_element_by_xpath(xpath)
        submit.click()


spider = CampaignSpider(election="municipal", position="mayor")
resp = spider.parse_all_election_data()
print resp