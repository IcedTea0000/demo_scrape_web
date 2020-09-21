from selenium import webdriver


class RedfinCrawler:
    def __init__(self):
        pass

    def get_browser(self):
        """return webdriver browser"""
        return webdriver.Chrome('C:\Remy Martin\workspace\WebScrapeCrawlProjects\drivers\chromedriver85.exe')

    def get_html(self, target_url):
        """return html of target url"""
        browser = self.get_browser()
        browser.get(target_url)
        html = browser.page_source
        browser.close()
        return html


if __name__ == '__main__':
    # execute script only
    url = 'https://www.redfin.com/'
    crawler = RedfinCrawler()
    print(crawler.get_html(target_url=url))
