from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re
import csv


class GuitarPlusCrawler:
    def __init__(self):
        self.internal_link_set = set()
        self.external_link_set = set()

    def generate_headers(self):
        """return human headers"""
        headers = {
            'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/85.0.4183.83 Safari/537.36',
            'ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8, application/signed-exchange;v=b3;q=0.9',
            'ACCEPT-ENCODING': 'gzip, deflate, br',
            'ACCEPT-LANGUAGE': 'en-US',
            'REFERER': 'https://www.google.com/'
        }
        return headers

    def get_soup(self, target_url):
        """create request to send, convert return response to soup object and return soup"""
        try:
            response = requests.get(url=target_url, headers=self.generate_headers())
            if response.status_code != 200:
                return None
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException:
            print('[Error] Error sending request to {}'.format(target_url))
        return None

    def convert_relative_path(self, current_url, path):
        """convert web page relative path to absolute path"""
        if path.startswith('/'):
            return self.get_domain(current_url) + path
        return path

    def get_domain(self, url):
        """extract domain from url"""
        parse = urlparse(url=url)
        return parse.scheme + '://' + parse.netloc

    def export_csv(self, store_path, contents):
        """export data to store as csv in local"""

    def get_hrefs_by_regex(self, soup, regex):
        """find all hrefs in <a> tag follow regex"""
        if soup is None:
            return None
        # get html from tag <body>
        body = soup.find(name='body')
        if body:
            # get all <a> tag contain attr href with regex
            a_tags = body.find_all(name='a', attrs={'href': regex})
            return a_tags
        return None

    def get_internal_links(self, target_url):
        """recursion to traverse all internal link from starter url"""
        self.internal_link_set.add(target_url)
        soup = self.get_soup(target_url=target_url)

        # get html from tag <a>
        href_regex = re.compile('(^https://guitarplus.com.*)'  # starts with 'https://guitarplus.com'
                                '|'  # or
                                '(^/.*)',  # start with '/'
                                re.IGNORECASE | re.VERBOSE)

        for a_tag in self.get_hrefs_by_regex(soup=soup, regex=href_regex):
            link = a_tag.attrs['href']
            link = self.convert_relative_path(current_url=target_url, path=link)
            if link not in self.internal_link_set:
                self.internal_link_set.add(link)
                print(link)
                self.get_internal_links(link)

    def get_external_links(self, target_url):
        """recursion to traverse all external link from starter url"""
        soup = self.get_soup(target_url=target_url)

        if soup is None:
            return None

        # get html from tag <a>
        href_regex = re.compile('(^https|http|www)'  # starts with https|http|www
                                '((?!guitarplus.com)'  # does not follow with 'guitarplus.com'
                                '.)*$',
                                re.IGNORECASE | re.VERBOSE)
        for a_tag in self.get_hrefs_by_regex(soup=soup, regex=href_regex):
            link = a_tag.attrs['href']
            self.external_link_set.add(link)
            print(link)


if __name__ == '__main__':
    # execute script only
    start_link = 'https://guitarplus.com/'
    guitarPlusCrawler = GuitarPlusCrawler()
    guitarPlusCrawler.get_internal_links(target_url=start_link)
