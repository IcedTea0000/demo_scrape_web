from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re


def generate_header():
    """return headers to create request"""
    headers = {
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'ACCEPT-ENCODING': 'gzip, deflate, br',
        'ACCEPT-LANGUAGE': 'en-US',
        'REFERER': 'https://www.google.com/'
    }
    return headers


def get_soup(absolute_path):
    """return beautiful soup object from input url"""
    try:
        response = requests.get(url=absolute_path, headers=generate_header())
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        print('[Error] error sending request')
        return None
    return soup


def convert_absolute_url(target_url):
    parse = urlparse(url=target_url)
    return parse.scheme + '://' + parse.netloc


def get_link(soup, target_url):
    """get a internal href from soup object"""
    links = set()
    domain = convert_absolute_url(target_url)

    if soup is not None:
        body = soup.find(name='body')
        a_hrefs = body.find_all(name='a', attrs={'href': re.compile('^\/wiki' #starts with '/wiki'
                                                                    '.*' # follow by any number of characters
                                                                    )})
        for link in a_hrefs:
            href = link.attrs['href']
            links.add(domain + href)

    return links


if __name__ == '__main__':
    # execute script only
    target_url = 'https://en.wikipedia.org/wiki/Data'
    links = get_link(get_soup(target_url), target_url)
    print(*links, sep='\n')
