from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class TmsAutoExplain:
    def __init__(self):
        pass

    def get_driver(self):
        local_path = 'C:\Remy Martin\workspace\WebScrapeCrawlProjects\drivers\chromedriver85.exe'
        return webdriver.Chrome(local_path)

    def log_in(self, url):
        username = 'nnhlam'
        password = 'Password563'

        timeout = 10
        browser = self.get_driver()
        browser.get(url)
        try:
            element_present = EC.presence_of_element_located((By.ID, 'password'))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

        element_username = browser.find_element_by_name(name='username')
        element_username.clear()
        element_username.send_keys(username)
        element_password = browser.find_element_by_name(name='password')
        element_password.clear()
        element_password.send_keys(password)

        login_btn = browser.find_element_by_class_name('btn-login')
        login_btn.click()
        print('[Info] Login to TMS account {} completed'.format(username))

        browser.get('https://tms.cmcglobal.com.vn/main/abnormalcase/index')

        browser.close()


if __name__ == '__main__':
    tms_bot = TmsAutoExplain()
    tms_bot.log_in('https://tms.cmcglobal.com.vn')
    print('test')
