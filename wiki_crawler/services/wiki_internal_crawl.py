from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re
import csv
from wiki_crawler.entities.objects import Link


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
        # send get request to url with headers
        response = requests.get(url=absolute_path, headers=generate_header())
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        print('[Error] Error sending request')
        return None
    return soup


def convert_absolute_url(target_url):
    """convert target url and get domain only"""
    parse = urlparse(url=target_url)
    return parse.scheme + '://' + parse.netloc


def write_to_csv(file_name, local_path, contents):
    """append contents to local file"""
    csv_file = open(local_path + '\\' + file_name, 'a', newline='')
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['Title', 'Url'])
    for link in contents:
        csv_writer.writerow([link.title,link.url])
    print('[Logger] File export successfully to {}'.format(local_path))
    csv_file.close()


def get_link(soup, target_url):
    """get a internal href from soup object"""
    links = set()
    domain = convert_absolute_url(target_url)

    if soup is not None:
        # get body of page source
        body = soup.find(name='body')
        # get all <a> contains href with internal link
        a_tags = body.find_all(name='a', attrs={'href': re.compile('^\/wiki'  # starts with '/wiki'
                                                                   '.*'  # follow by any number of characters
                                                                   )})
        # get href part in <a> and convert to full url
        for a_tag in a_tags:
            href = a_tag.attrs['href']
            try:
                title = a_tag.attrs['title']
            except:
                title = ''
            link = Link(url=domain + href, title=title)
            links.add(link)

    return links


if __name__ == '__main__':
    # execute script only
    target_url = 'https://en.wikipedia.org/wiki/Data'
    link_list = get_link(get_soup(target_url), target_url)
    write_to_csv(file_name='wiki.csv', local_path='..\..\io', contents=link_list)
