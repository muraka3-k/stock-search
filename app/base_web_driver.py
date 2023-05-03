from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
from bs4 import BeautifulSoup

class BaseWebDriver:
    driver = None
    base_url = ""
    def __init__(self, url:str = None):
        if url is None:
            return
        self.driver = webdriver.Chrome()
        self.base_url = url

    def closeWindow(self):
        self.driver.close()

    def jumpBaseURL(self):
        self.driver.get(self.base_url)
    ### wait_element関数
    ### [in]driver：webdriverや抽出する要素を入力
    ### [in]by_id：待機する要素の検索するID（By.TAG_NAME、By.CLASS_NANE等）
    ### [in]name：探索する要素の名称
    ### [in]timeout：タイムアウトまで待つ時間
    ### [out]探索した要素
    def wait_element(self, driver:webdriver, by_id:By, name:str, timeout:int = 30):
         return WebDriverWait(driver, timeout).until(
             EC.presence_of_element_located((by_id, name))
             )
    ### JavaScriptで記載されたJSON部分を抽出する関数
    ### [in] driver：webdriver（page_sourceを取得するため必須）
    ### [in] label_list：抽出したいソースでテキスト化されているリスト
    def find_javascript_json(self, driver:webdriver, label_list = []):
        json_script = None
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        elements = soup.select('script')

        for element in elements:
            flag = True
            for label in label_list:
                if label not in str(element):
                    flag = False
            if flag:
                json_script = json.loads(element.string.split("=")[1].split(";")[0])
                break
        
        return json_script


