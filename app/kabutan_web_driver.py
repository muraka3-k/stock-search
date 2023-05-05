from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import sys
import time
import json

from base_web_driver import BaseWebDriver

class KabutanWebDrive(BaseWebDriver):
    wait_time_element = 0

    def __init__(self, url:str = None):
        ### kabutanは待ち時間5秒にする
        super().__init__(url, wait_next_page = 5)
        self.wait_time_element = 3
        print("wait time for next element:", self.wait_time_element)

    ### チャートのメニューから入力文字（button_name）をクリックする処理
    def jumpChartMenu(self, button_name):
        chart_menu = self.wait_element(self.driver, By.CLASS_NAME, "chart_menu")
        chart_menu.find_element(By.LINK_TEXT, button_name).click()
        time.sleep(self.wait_time_element)

    ### 銘柄コードを入力してトップ画面へ移行する
    def jumpTickerTopPage(self, ticker_code: int):
            top_key = self.wait_element(self.driver, by_id = By.CLASS_NAME, name = "kensaku_input").find_element(By.ID, "input_id")
            top_key.send_keys(ticker_code)
            top_key.send_keys(Keys.ENTER)
            time.sleep(self.wait_new_page)
            self.jumpChartMenu("基本情報")
            return

    ### 株価情報を取得する処理
    def extractPriceData(self):
        element_company = self.wait_element(self.driver, By.ID, "stockinfo")
        stock_price = element_company.find_element(By.CLASS_NAME, "kabuka").text.split("円")[0]
        # stock_price = self.driver.find_element(By.CLASS_NAME, "kabuka")
        return stock_price

    def extractCompanyInfo(self, ticker_code: int):
        self.jumpChartMenu("基本情報")
        element_company = self.wait_element(self.driver, By.ID, "stockinfo")

        kind = element_company.find_element(By.ID, "stockinfo_i2").find_elements(By.TAG_NAME, "a")[0].text
        name = element_company.find_element(By.CLASS_NAME, "si_i1_1").find_element(By.TAG_NAME, "h2").text.split(str(ticker_code))[1]

        return { "業種": kind, "会社名": name}
   
    ### テーブル情報を取得するための関数
    def __extractTableInfo(self, head_ele, body_ele, ext_list):
        table = []
        for i, tr in enumerate(body_ele.find_elements(By.TAG_NAME, "tr")):
            if len(tr.find_elements(By.TAG_NAME, "th")) == 0:
                continue
            if "前期比" in tr.find_elements(By.TAG_NAME, "th")[0].text:
                continue
            tmp_json = {}
            tmp_json["決算期"] = tr.find_elements(By.TAG_NAME, "th")[0].text.split("\u3000")[-1].replace(" ", "")
            for ext in ext_list:
                for j, th in enumerate(head_ele.find_elements(By.TAG_NAME, "th")):
                    if ext[0] in th.text:
                        tmp_json[ext[1]] = tr.find_elements(By.TAG_NAME, "td")[j - 1].text
            print(tmp_json)
            table.append(tmp_json)
        return table

    ### 決算のテーブル情報を取得するための関数（__extractTableInfoを呼び出す）
    def extractFinanceResult(self, table_element, ext_list):
        head_ele = table_element.find_element(By.TAG_NAME, "thead")
        body_ele = table_element.find_element(By.TAG_NAME, "tbody")

        return self.__extractTableInfo(head_ele, body_ele, ext_list)

    def __extractTableinFinanceResult(self, str_page: str, str_table: str, extract_list):
        self.jumpChartMenu("決算")
        fin_box_element = self.wait_element(self.driver, By.ID, "finance_box")

        ### 通期タブの中の"str_page"のページを表示する
        for ele in fin_box_element.find_elements(By.CLASS_NAME, str_page.split(" ")[0]):
            if ele.get_attribute("class") == str_page:
                ele.click()

        ### "str_page"に対応する"str_table"テーブル要素を取得する
        for ele in fin_box_element.find_elements(By.CLASS_NAME, str_table.split(" ")[0]):
            if ele.get_attribute("class") == str_table:
                table_ele = ele

        return self.extractFinanceResult(table_ele, extract_list)

    ### 決算情報からキャッシュフロー情報を抽出する関数
    def __extractCacheFlowTable(self, ext_list):
        self.jumpChartMenu("決算")
        fin_box_element = self.wait_element(self.driver, By.ID, "finance_box")

        for element in fin_box_element.find_elements(By.TAG_NAME, "table"):
            if len(element.find_elements(By.TAG_NAME, "thead")) == 0:
                continue
            head_ele = element.find_element(By.TAG_NAME, "thead")
            flag = True
            for label in ext_list:
                if label[0] not in head_ele.text:
                    flag = False
            if flag:
                body_ele = element.find_element(By.TAG_NAME, "tbody")
                break

        return self.__extractTableInfo(head_ele, body_ele, ext_list)

    ### 基本情報ページからPER,PBR,利回りを抽出
    def extractPERforTable(self):    
        extract_list =[
            ["PER", "倍"],
            ["PBR", "倍"],
            ["利回り", "％"]
        ]
        self.jumpChartMenu("基本情報")
        element_company = self.wait_element(self.driver, By.ID, "stockinfo")

        output_json = {}
        table_ele = element_company.find_element(By.ID, "stockinfo_i3")
        for i, th in enumerate(table_ele.find_elements(By.TAG_NAME, "th")):
            for ext in extract_list:
                if ext[0] in th.text:
                    output_json[ext[0]] = table_ele.find_elements(By.TAG_NAME, "td")[i].text.split(ext[1])[0]
        return output_json

    ### 基本情報ページからEPS,配当を抽出
    def extractEPSinforTopPage(self):
        extract_list =[
            ["１株益", "EPS"],
            ["１株配", "配当"]
        ]
        self.jumpChartMenu("基本情報")
        kobetsu_element = self.wait_element(self.driver, By.ID,   "kobetsu_right")
        gyoseki_ele = kobetsu_element.find_element(By.CLASS_NAME, "gyouseki_block")
        table_ele   = gyoseki_ele.find_element    (By.TAG_NAME,   "table")

        return {"業績": self.extractFinanceResult(table_ele, extract_list)}

    ### 決算情報からEPS/配当を抽出する関数
    def extractEPSinFinanceResult(self):
        extract_list =[
            ["修正1株益", "EPS"],
            ["１株配", "配当"]
        ]
        str_page = "fin_year_result"                  ### 業務推移のタブ移動用
        str_table = "fin_year_t0_d fin_year_result_d" ### 今期の業績予想のテーブル情報
        return {"業績": self.__extractTableinFinanceResult(str_page, str_table, extract_list)}

    ### 決算情報からROE/ROAを抽出する関数
    def extractROEinFinanceResult(self):
        extract_list =[
            ["営業益", "営業益"],
            ["ＲＯＥ", "ROE"],
            ["ＲＯＡ", "ROA"]
        ]
        
        str_page = "fin_year_profit"   ### 収益性のタブ移動用
        str_table = "fin_year_t0_d fin_year_profit_d dispnone" ### 収益性のテーブル情報
        return {"収益性": self.__extractTableinFinanceResult(str_page, str_table, extract_list)}

    ### 決算情報からCFを抽出する関数
    def extractCacheFlowResult(self):
        extract_list =[
            ["営業CF", "営業CF"],
            ["投資CF", "投資CF"],
            ["フリーCF", "フリーCF"],
            ["財務CF", "財務CF"]
        ]

        return {"CF": self.__extractCacheFlowTable(extract_list)}

    ### 銘柄コードから株価情報を取得するメイン関数
    def searchTickerPage(self, ticker_code:int = 0):
        result_json = {}

        ### トップページに遷移する
        self.jumpBaseURL()

        ### 銘柄ページへ移動する
        self.jumpTickerTopPage(ticker_code)

        ### 業種情報取得
        result_json["銘柄コード"] = ticker_code
        result_json.update(self.extractCompanyInfo(ticker_code))
        print("業種:", result_json["業種"])
        print("会社名:", result_json["会社名"])

        result_json["株価"] = self.extractPriceData()
        print("株価：", result_json["株価"])

        ### 基本情報ページからPER,PBR,利回りを抽出
        result_json.update(self.extractPERforTable())

        ### 基本情報ページからEPS,配当を抽出
        result_json.update(self.extractEPSinforTopPage())

        ### 決算情報からEPS/配当を抽出
        result_json.update(self.extractEPSinFinanceResult())

        ### 決算情報からROE/ROAを抽出
        result_json.update(self.extractROEinFinanceResult())

        ### 決算情報からキャッシュフロー情報を抽出
        result_json.update(self.extractCacheFlowResult())
        
        return result_json

if __name__ == "__main__": 
    if len(sys.argv[1:]) != 0:
        ticker_list = [int(ticker) for ticker in  sys.argv[1:]]
    else:
      ticker_list = [2914, 9104]
    print("search ticker:", ticker_list)

    url = "https://kabutan.jp/"
    wd = KabutanWebDrive(url)
    result = []
    for ticker in ticker_list:
        result.append(wd.searchTickerPage(ticker))

    with open('search_result.json', 'w') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
