from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin
import re
import csv
import sys
import os
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class BookToScrapeCrawler:
    def __init__(self):
        self.internal_links = set()
        self.external_link = set()

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
        """send request and return a BeautifulSoup object"""
        try:
            response = requests.get(url=target_url, headers=self.generate_headers())
            if response.status_code != 200:
                return None
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException:
            print('[Error] Error sending request to {}'.format(target_url))
        return None

    def extract_href_by_regex(self, soup, regex_pattern):
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

    def get_all_href(self, target_url):
        """print set of all hrefs in page. Use to check href pattern of web page"""
        href_regex = re.compile('.*')
        soup = self.get_soup(target_url=target_url)
        href_set = set()
        for link in self.extract_href_by_regex(soup=soup, regex_pattern=href_regex):
            if link.attrs['href']:
                href_set.add(link.attrs['href'])
        print(*href_set, sep='\n')

    def collect_internal_links(self, starting_url):
        """recursion to extract all internal links to set"""
        href_regex = re.compile('.*')
        soup = self.get_soup(target_url=starting_url)
        for a_tag in self.extract_href_by_regex(soup=soup, regex_pattern=href_regex):
            if a_tag.attrs['href']:
                # convert href to absolute path
                link = urljoin(starting_url, a_tag.attrs['href'])
                if link not in self.internal_links:
                    self.internal_links.add(link)
                    print(link)
                    self.collect_internal_links(starting_url=link)
        return

    def collect_external_links(self):
        return

    def export_csv(self, file_name, local_path):
        """write internal links set to csv file"""
        # Open a file for writing. Creates a new file if it does not exist or truncates the file if it exists
        csv_file = open(os.path.join(local_path, file_name), 'w', newline='')
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(['Url'])
        for link in self.internal_links:
            csv_writer.writerow([link])
        print('[Logger] File export successfully to {}'.format(local_path))
        csv_file.close()

    def get_connection(self, host, username, password):
        """return a connection to mysql database"""
        return mysql.connector.connect(host=host, user=username, password=password)

    def insert_to_db(self):
        """insert internal links set to db"""
        connection = self.get_connection('127.0.0.1', 'root', 'root')
        mycursor = connection.cursor()
        for link in self.internal_links:
            mycursor.execute("""INSERT INTO crawler_import.book_to_scrape
                            (`url`)
                            VALUES
                            ('""" + link + """');
                            """)
            connection.commit()
        mycursor.close()
        print('[Logger] Finish writing internal links set to database')


class BookToScrapeCrawlerSelenium:
    def __init__(self):
        pass

    def get_browser(self):
        """return selenium chrome driver"""
        local_path = 'C:\Remy Martin\workspace\WebScrapeCrawlProjects\drivers\chromedriver85.exe'
        return webdriver.Chrome(executable_path=local_path)

    def test(self):
        browser = self.get_browser()
        browser.get(url='http://books.toscrape.com/')
        # element = browser.find_element_by_name('q')
        # element.clear()
        # element.send_keys('test')
        # element.send_keys(Keys.ENTER)

        body = browser.find_element_by_tag_name('body')

        next_btn = browser.find_element_by_xpath(xpath='//*[@id="default"]/div/div/div/div/section/div[2]/div/ul/li[2]/a')
        next_btn.click()
        print('test')

if __name__ == '__main__':
    # execute script only
    # set new recursion limit
    sys.setrecursionlimit(10 ** 2)

    url = 'http://books.toscrape.com'

    # crawler = BookToScrapeCrawler()
    # try:
    #     crawler.collect_internal_links(starting_url=url)
    # except RecursionError:
    #     pass
    # # print(*crawler.internal_links, sep='\n')
    # crawler.export_csv(file_name='temp_html_scrape.html', local_path='C:/remy_temp/')
    # crawler.insert_to_db()

    crawler = BookToScrapeCrawlerSelenium()
    crawler.test()
