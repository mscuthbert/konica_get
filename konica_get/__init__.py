from enum import Enum
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

class WaitTime(Enum):
    SHORT = 5
    MEDIUM = 20
    LONG = 30
    ONE_HOUR = 3600

class KonicaGet:
    def __init__(self, *, server: str, headless: bool = True):
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')
        else:
            chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.server = server
        self.box_login = '/wcd/box_login.xml'

    def __del__(self):
        self.driver.close()

    def el(self, selector, wait_time=WaitTime.MEDIUM) -> WebElement:
        return WebDriverWait(self.driver, wait_time.value).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    def get_all_docs(self, delete=False):
        self.open_box()
        time.sleep(7)
        i = 0
        while True:
            try:
                self.el(f'#F_UOU_ThumbnailOn_CHK{i}')
            except TimeoutException:
                break
            self.download_doc_by_index(i)
            if delete:
                self.delete_doc_by_index(i)
            else:
                i += 1

    def open_box(self, number=1348):
        self.driver.get(self.server + self.box_login)
        box = self.el('.box-input-no input')
        time.sleep(3)
        box.send_keys(str(number))
        ok_button = self.el('.box-inputok input')
        time.sleep(3)
        ok_button.click()

    def download_doc_by_index(self, index=0):
        select_first = self.el(f'#F_UOU_ThumbnailOn_CHK{index}', wait_time=WaitTime.LONG)
        time.sleep(3)
        select_first.click()
        download_btn = self.el('#F_UOU_ToolBarDownloadBtn')
        time.sleep(3)
        download_btn.click()
        continue_btn = self.el('#comButtonAreaJobOperate input')
        time.sleep(3)
        continue_btn.click()
        download_btn = self.el('#btnEXE', wait_time=WaitTime.ONE_HOUR)
        time.sleep(3)
        download_btn.click()
        time.sleep(20)
        back_to_menu = self.el('#downloadbtnOK')
        time.sleep(3)
        back_to_menu.click()

    def delete_doc_by_index(self, index):
        select_first = self.el(f'#F_UOU_ThumbnailOn_CHK{index}', wait_time=WaitTime.LONG)
        time.sleep(3)
        select_first.click()
        delete_btn = self.el('#F_UOU_ToolBarDeleteBtn')
        time.sleep(3)
        delete_btn.click()
        continue_btn = self.el('#comButtonAreaJobOperate input')
        time.sleep(3)
        continue_btn.click()
        done_btn = self.el('#cgierrorbtnOK')
        time.sleep(3)
        done_btn.click()


if __name__ == '__main__':
    kg = KonicaGet(headless=False)
    kg.get_all_docs(delete=True)
    del kg

