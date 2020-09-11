from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re
import csv


class GuitarPlusCrawler:
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

    link_set = set()

    def get_links(self, target_url):
        """recursion to traverse all internal link from starter url"""
        soup = self.get_soup(target_url=target_url)

        if soup is None:
            return None

        # get html from tag <body>
        body = soup.find(name='body')
        # get html from tag <a>
        href_regex = re.compile('(^https://guitarplus.com.*)'  # starts with 'https://guitarplus.com'
                                '|'  # or
                                '(^/.*)',  # start with '/'
                                re.IGNORECASE | re.VERBOSE)
        if body:
            a_tags = body.find_all(name='a', attrs={'href': href_regex})
            if a_tags:
                for a_tag in a_tags:
                    link = a_tag.attrs['href']
                    if link.startswith('/'):
                        link = self.convert_relative_path(current_url=target_url, path=link)
                    if link not in self.link_set:
                        self.link_set.add(link)
                        print(link)
                        self.get_links(link)

    def get_link(self, url):
        """recursion to traverse all internal link from starter url"""
        """extract all internal links in web page, return set of all links"""
        all_link_set = set()

        soup = self.get_soup(target_url=url)
        if soup is None:
            return None
        link_set = self.get_link(soup)

        return sorted(all_link_set)

    def convert_relative_path(self, current_url, path):
        """convert web page relative path to absolute path"""
        return self.get_domain(current_url) + path

    def get_domain(self, url):
        """extract domain from url"""
        parse = urlparse(url=url)
        return parse.scheme + '://' + parse.netloc

    def export_csv(self, store_path, contents):
        """export data to store as csv in local"""


if __name__ == '__main__':
    # execute script only
    start_link = 'https://guitarplus.com/'
    guitarPlusCrawler = GuitarPlusCrawler()
    guitarPlusCrawler.get_links(target_url=start_link)
