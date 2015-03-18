import time
from selenium import webdriver
from selenium.webdriver.support.select import Select


class ElectionSpider(object):
    name = 'ElectionSpider'
    allowed_domains = ['http://www.chicagoelections.com']
    start_urls = ['http://www.chicagoelections.com/en/election3.asp']

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self):
        self.driver.get('http://www.chicagoelections.com/en/election3.asp')
        # time.sleep(10)
        try:
            main_dropdown = self.driver.find_element_by_xpath('//select[@name="D3"]')
            for option in main_dropdown.find_elements_by_tag_name('option'):
                if option.text == "2015 Municipal General - 2/24/15":
                    option.click()
                    print "we clicked!"
                    break
            submit = self.driver.find_element_by_xpath('//input[@type="submit"]')
            submit.click()
            # time.sleep(25)
            current_yr_dropdown = self.driver.find_element_by_xpath('//select[@name="D3"]')
            for option in current_yr_dropdown.find_elements_by_tag_name('option'):
                if option.text == "Mayor":
                    option.click()
                    print "we clicked again!"
                    break
            view_mayor_submit = self.driver.find_element_by_xpath('//input[@value="  View The Results   "]')
            view_mayor_submit.click()
            data = []
            for tr in self.driver.find_elements_by_xpath('//table[@width="100%"]//tr'):
                tds=tr.find_elements_by_tag_name('td')
                if tds:
                    print "yup found td"
                    data.append([td.text for td in tds])
            time.sleep(25)
        except:
            pass
        print data

        self.driver.close()

spider = ElectionSpider()
resp = spider.parse()