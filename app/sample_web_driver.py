from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import time
import json

from base_web_driver import BaseWebDriver

class SampleWebDrive(BaseWebDriver):
    def __extractCorpInfo(self, driver):
        bread = driver.find_element(By.CLASS_NAME, "breadcrumb")
        kind = bread.find_elements(By.TAG_NAME, "li")[2].text
        name = bread.find_elements(By.TAG_NAME, "li")[3].text.split("【")[0]

        return kind, name
    
    def __extractPERinfo(self, driver, result_json):
        ### 表からPER,ROE,配当利回りを抽出
        extract_list =[
            ["PER", "倍"],
            ["ROE", "%"],
            ["配当利回り", "%"]
        ]

        for ele in driver.find_elements(By.CLASS_NAME, "col-lg-2"):
            for ext in extract_list:
                if ext[0] in ele.text:
                    result_json[ext[0]] = ele.text.split(ext[1])[0]
                    print(ext[0], ":",result_json[ext[0]])

    def __extractDividendSummary(self, driver, result_json):
        str_div = "{}･{}".format("配当", "会予")
        for ele in driver.find_elements(By.CLASS_NAME, "table"):
            if str_div in ele.text:
                for tr in ele.find_elements(By.TAG_NAME, "tr"):
                    if str_div in tr.text:
                        result_json[str_div] = tr.find_elements(By.TAG_NAME, "td")[1].text.split("円")[0]
                        print(str_div, "：", result_json[str_div])
            if "配当性向" in ele.text:
                for tr in ele.find_elements(By.TAG_NAME, "tr"):
                    if "配当性向" in tr.text:
                        result_json["配当性向"] = tr.find_elements(By.TAG_NAME, "td")[1].text
                        print("配当性向：", result_json["配当性向"])

    def __extractDividendData(self, driver):
        output = []
        str_class = "{}-{}-{}".format("data",   "react",    "class")
        str_chart = "{}/{}{}" .format("charts", "Dividend", "Chart")
        str_props = "{}-{}-{}".format("data",   "react",    "props")

        ### 配当チャートの抽出
        for div in driver.find_elements(By.TAG_NAME, "div"):
            if div.get_attribute(str_class) == str_chart:
                dividend_chart = ''.join(div.get_attribute(str_props)).splitlines()[0]
                break
        json_dev = json.loads(dividend_chart)

        for data in json_dev["series"]:
            if data["name"] == "配当":
                div_data = data["data"]
            if data["name"] == "配当性向":
                payout_rate = data["data"]
        
        for i,data in enumerate(div_data):
            output.append({
                "日付":div_data[i]["name"],
                "配当":div_data[i]["y"],
                "配当性向":payout_rate[i]["y"]
            })
        return output
    

    def __extractCacheData(self, driver):
        output = []
        label_list = ["営業CF", "投資CF", "フリーCF"]
        json_cache = self.find_javascript_json(driver, label_list)

        tmp_data=[]
        for data in json_cache["series"]:
            for label in label_list:
                if data["name"] == label:
                    tmp_data.append(data["data"])
        
        for i in range(len(tmp_data[0])):
            tmp_json = {}
            for j, label in enumerate(label_list):
                tmp_json["日付"] = tmp_data[j][i][0]
                tmp_json[label] = tmp_data[j][i][0]
            output.append(tmp_json)

        return output

    def pageJumpSideBar(self, driver, jump_str:str):
        str_side = "{}--{}_{}".format("sidebar", "company", "_body")
        side_bar = self.wait_element(driver, By.CLASS_NAME, str_side)
        side_bar.find_element(By.LINK_TEXT, jump_str).click()
        time.sleep(2)


    def searchTickerPage(self, ticker_code:int = 0):
        result_json = {}

        ##" 要素探索用の文字列"
        str_company    = "{}-{}-{}".format("body", "container", "-company")
        str_top_search = "{}_{}-{}".format("top_", "search", "column")

        self.jumpBaseURL()
        time.sleep(1)

        self.top_key_element = self.wait_element(
            self.driver, by_id = By.CLASS_NAME, name = str_top_search
            ).find_element(By.NAME, "keyword")
        self.top_key_element.send_keys(ticker_code)

        time.sleep(1)
        self.top_key_element.send_keys(Keys.ENTER)

        element_company = self.wait_element(
            self.driver, By.CLASS_NAME, str_company
            )
        
        result_json["銘柄コード"] = ticker_code

        ### 企業情報の取得
        info = self.__extractCorpInfo(element_company)
        result_json["業種"]  = info[0]
        result_json["会社名"] = info[1]
        print("業種", result_json["業種"])
        print("会社名", result_json["会社名"])

        result_json["株価"] = element_company.find_element(By.ID, "stockprice").text
        print("株価：", result_json["株価"])

        self.__extractDividendSummary(element_company, result_json)
        self.__extractPERinfo(element_company, result_json)
        result_json["配当履歴"] = self.__extractDividendData(element_company)

        self.pageJumpSideBar(self.driver, "業績")
        self.wait_element(self.driver, By.CLASS_NAME, str_company)
        result_json["CF"] = self.__extractCacheData(self.driver)

        return result_json

if __name__ == "__main__": 
    url = ""
    ticker_list = [2914, 9104]
    wd = SampleWebDrive(url)
    wd.searchTickerPage(ticker_list[0])
