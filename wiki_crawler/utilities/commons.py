from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re
import csv


def generate_headers():
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


def get_soup(target_url):
    """send request and return a BeautifulSoup object"""
    try:
        response = requests.get(url=target_url, headers=generate_headers())
        if response.status_code != 200:
            return None
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException:
        print('[Error] Error sending request to {}'.format(target_url))
    return None


def extract_href_by_regex(soup, regex_pattern):
    """return set of all a tags with href in soup filtered by regex"""
    links = set()
    if soup is None:
        return None
    body = soup.find(name='body')
    if body:
        # get all <a> tag contain attr href with regex
        links = body.find_all(name='a', attrs={'href': regex_pattern})
        return links
    return None


def get_all_href(target_url):
    """print set of all hrefs in page. Use to check href pattern of web page"""
    href_regex = re.compile('.*')
    soup = get_soup(target_url=target_url)
    href_set = set()
    for link in extract_href_by_regex(soup=soup, regex_pattern=href_regex):
        if link.attrs['href']:
            href_set.add(link.attrs['href'])
    print(*href_set, sep='\n')


if __name__ == '__main__':
    # execute script only
    url = '../../../the-red-tent_273/index.html'
