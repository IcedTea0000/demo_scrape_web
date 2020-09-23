from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin
import re
import csv


class RedfinCrawler:
    def __init__(self):
        self.filter_price_list = ['0k', '50k', '75k', '100k', '125k', '150k', '175k', '200k', '225k', '250k',
                                  '275k', '300k', '325k', '350k', '375k', '400k', '425k', '450k', '475k', '500k',
                                  '550k', '600k', '650k', '700k', '750k', '800k', '850k', '900k', '950k', '1M',
                                  '1.25M', '1.5M', '1.75M', '2M', '2.25M', '2.5M', '2.75M', '3M', '3.25M', '3.5M',
                                  '3.75M', '4M', '4.25M', '4.5M', '4.75M', '5M', '6M', '7M', '8M', '9M', '10M']
        self.domain = 'https://www.redfin.com/'
        self.filter_location = '/city/7178/TX/Galveston'
        self.filter_property = '/filter/property-type=house+condo+townhouse+multifamily'

    def get_browser(self):
        """return webdriver browser"""
        return webdriver.Chrome('C:\workspace\drivers\chromedriver85.exe')

    def get_target_url(self, min_price, max_price):
        """return full url of redfin with filters composed from min price, max price"""
        filter_others = ',min-price=' + min_price + ',max-price=' + max_price + ',include=sold-5yr'
        return urljoin(self.domain, self.filter_location + self.filter_property + filter_others)

    def get_html(self, target_url):
        """return html of target url"""
        browser = self.get_browser()
        browser.get(target_url)
        html = browser.page_source
        browser.close()
        return html

    def temp(self, html):
        """extract price from all option tag for filter"""
        price_list = []
        soup = BeautifulSoup(html, 'html.parser')
        options = soup.find_all(name='option')
        for option_tag in options:
            if option_tag.getText() is not None:
                price_list.append(option_tag.getText())
        print(price_list)
        return


if __name__ == '__main__':
    # execute script only
    url = 'https://www.redfin.com/city/4001/TX/Cleveland'
    crawler = RedfinCrawler()
    print(crawler.get_target_url(min_price='50k', max_price='75k'))
