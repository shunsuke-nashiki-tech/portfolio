import csv
import math
import datetime
import urllib
import random
import regex
import requests
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

#要素を取得
class Get_data:
    
    def __init__(self,url_adress):

        #グローバル変数を生成
        global get_date_list #取得日 
        global detail_url_list #詳細URL
        global seach_title_list #検索タイトル
        global shop_name_list #店舗名
        global first_janre_list #ジャンル1
        global second_janre_list #ジャンル2
        global third_janre_list #ジャンル3
        global four_janre_list #ジャンル4
        global evaluation_list #評価
        global prefectures_list #都道府県
        global street_adress_list #住所
        global tel_number_list #電話番号
        global budget_lunch_lower_list #予算_昼_下限
        global budget_lunch_upper_list #予算_昼_上限
        global budget_dinner_lower_list #予算_夜_下限
        global budget_dinner_upper_list #予算_夜_上限
        
        #リストを生成・初期化
        get_date_list = [] #取得日 
        detail_url_list = [] #詳細URL
        seach_title_list = [] #検索タイトル
        shop_name_list = [] #店舗名
        first_janre_list = [] #ジャンル1
        second_janre_list = [] #ジャンル2
        third_janre_list = [] #ジャンル3
        four_janre_list = [] #ジャンル4
        evaluation_list = [] #評価
        prefectures_list = [] #都道府県
        street_adress_list = [] #住所
        tel_number_list = [] #電話番号
        budget_lunch_lower_list = [] #予算_昼_下限
        budget_lunch_upper_list = [] #予算_昼_上限
        budget_dinner_lower_list = [] #予算_夜_下限
        budget_dinner_upper_list = [] #予算_夜_上限

        #BeautifulSoupで取得
        self.url_adress = url_adress
        
        while True:
            try:
                self.html = urllib.request.urlopen(url_adress)
            except:
                print("requestに失敗しました。{}秒後に再取得を行います".format(failure_wait_time))
                time.sleep(failure_wait_time)
            else:
                self.soup = BeautifulSoup(self.html, 'lxml')
                time.sleep(succses_wait_time)
                break


    #ページ数を取得
    def page_count(self) ->int:

        #全件数を取得して、1ページの要素数（20件）で除算
        for table in self.soup.findAll(class_="list-condition__count"):
            self.page_count = re.sub(",","",table.text)
            self.page_count = math.ceil(int(self.page_count) / 20)
            
        return self.page_count

    #取得日、詳細URL、エリア名を取得
    def url_data(self):
        
        #「詳細URL」を取得して格納
        for table in self.soup.findAll(class_="list-rst__header"):
            for parts in table.findAll(class_="list-rst__rst-name-target cpy-rst-name"):
                self.detail_url = parts.get("href")
                detail_url_list.append(self.detail_url)

        #検索タイトルを取得
        for table in self.soup.findAll(class_="list-condition__title"):
            self.seach_title = re.sub("\r|\t|\n|\u3000|\xa0| ","",table.text)
            self.seach_title = self.seach_title.split("のお店")[0] #「のお店、レストラン」をsplit

        #URLリストの数だけ「取得日」「検索タイトル」を格納
        for append in detail_url_list:
            #取得日を格納
            get_date_list.append(date_time)
            #検索タイトルを格納
            seach_title_list.append(self.seach_title)

    #全ての要素を取得
    def all_data(self):

        #「取得日」を取得して格納
        get_date_list.append(csv_input_list["取得日"][csv_output_list_last_row])

        #「求人詳細URL」を取得して格納
        detail_url_list.append(csv_input_list["詳細URL"][csv_output_list_last_row])

        #「検索タイトル」を取得して格納
        seach_title_list.append(csv_input_list["検索タイトル"][csv_output_list_last_row])

        #店舗名を取得
        for table in self.soup.findAll(class_="rstinfo-table"):
            for shop_name_sub in table.findAll("tr"):
                for parts in shop_name_sub.findAll("th"):
                    if regex.findall("店名",parts.text):
                        self.shop_name = shop_name_sub.find("td")
                        self.shop_name = re.sub("\r|\t|\n|\u3000|\xa0| ","",self.shop_name.text)
                        shop_name_list.append(self.shop_name)

        #ジャンルを取得
        for table in self.soup.findAll(class_="rstinfo-table"):
            for janre_sub in table.findAll("tr"):
                for parts in janre_sub.findAll("th"):
                    if regex.findall("ジャンル",parts.text):
                        self.janre = janre_sub.find("td")
                        self.janre = re.sub("\r|\t|\n|\u3000|\xa0| ","",self.janre.text)

                        #ジャンル1を取得
                        try:
                            self.first_janre = self.janre.split("、")[0]
                        except:
                            self.first_janre = ""

                        first_janre_list.append(self.first_janre)

                        #ジャンル2を取得
                        try:
                            self.second_janre = self.janre.split("、")[1]
                        except:
                            self.second_janre = ""

                        second_janre_list.append(self.second_janre)

                        #ジャンル3を取得
                        try:
                            self.third_janre = self.janre.split("、")[2]
                        except:
                            self.third_janre = ""

                        third_janre_list.append(self.third_janre)

                        #ジャンル4を取得
                        try:
                            self.four_janre = self.janre.split("、")[3]
                        except:
                            self.four_janre = ""

                        four_janre_list.append(self.four_janre)

        #評価を取得
        for table in self.soup.findAll(class_="rdheader-counts-wrap"):
            for parts in table.findAll(class_="rdheader-rating__score-val-dtl"):
                self.evaluation = re.sub("\r|\t|\n|\u3000|\xa0| ","",parts.text)
                evaluation_list.append(self.evaluation)

        #都道府県を取得
        for table in self.soup.findAll(class_="rstinfo-table"):
            for prefectures_sub in table.findAll("tr"):
                for parts in prefectures_sub.findAll("th"):
                    if regex.findall("住所",parts.text):
                        self.prefectures = prefectures_sub.find("td").find("a")
                        self.prefectures = re.sub("\r|\t|\n|\u3000|\xa0|","",self.prefectures.text)
                        prefectures_list.append(self.prefectures)
                
        #住所を取得
        for table in self.soup.findAll(class_="rstinfo-table"):
            for street_address_sub in table.findAll("tr"):
                for parts in street_address_sub.findAll("th"):
                    if regex.findall("住所",parts.text):
                        self.street_address = street_address_sub.find("td").find("p")
                        self.street_address = re.sub("\r|\t|\n|\u3000|\xa0|","",self.street_address.text)
                        street_adress_list.append(self.street_address)

        #電話番号を取得
        for table in self.soup.findAll(class_="rstdtl-side-yoyaku__tel-number"):
            self.tel_number = re.sub("\r|\t|\n|\u3000|\xa0| ","",table.text)
            tel_number_list.append(self.tel_number)

        #予算を取得
        for table in self.soup.findAll(class_="rstinfo-table"):
            for budget_sub in table.findAll("tr"):
                for parts in budget_sub.findAll("th"):
                    parts = re.sub(" ","",parts.text)
                    if parts == "予算":
                        for budget in budget_sub.findAll("td"):

                            try:
                                #ランチの予算を取得                                
                                self.budget_lunch = budget.find(class_="gly-b-lunch")
                                self.budget_lunch = re.sub("\r|\t|\n|\u3000|\xa0| ","",self.budget_lunch.text)
                                
                                #下限を取得
                                try:
                                    self.budget_lunch_lower = self.budget_lunch.split("～")[0]
                                except:
                                    self.budget_lunch_lower = self.budget_lunch

                                #上限を取得
                                try:
                                    self.budget_lunch_upper = self.budget_lunch.split("～")[1]
                                except:
                                    self.budget_lunch_upper = self.budget_lunch
                            except:
                                #ランチの予算が取得できなければ、それぞれ空要素を格納
                                self.budget_lunch_lower = ""
                                self.budget_lunch_upper = ""
                            
                            #それぞれを格納
                            budget_lunch_lower_list.append(self.budget_lunch_lower)
                            budget_lunch_upper_list.append(self.budget_lunch_upper)
                                
                            try:
                                #ディナーの予算を取得
                                self.budget_dinner = budget.find(class_="gly-b-dinner")
                                self.budget_dinner = re.sub("\r|\t|\n|\u3000|\xa0| ","",self.budget_dinner.text)
                            
                               #下限を取得
                                try:
                                    self.budget_dinner_lower = self.budget_dinner.split("～")[0]
                                except:
                                    self.budget_dinner_lower = self.budget_dinner
                            
                                #上限を取得
                                try:
                                    self.budget_dinner_upper = self.budget_dinner.split("～")[1]
                                except:
                                    self.budget_dinner_upper = self.budget_dinner
                            except:
                                #ディナーの予算が取得できなければ、それぞれ空要素を格納
                                self.budget_dinner_lower = ""
                                self.budget_dinner_upper = ""
                            
                            #それぞれを格納
                            budget_dinner_lower_list.append(self.budget_dinner_lower)
                            budget_dinner_upper_list.append(self.budget_dinner_upper)


#url_listをアウトプット
def create_csv_url_list(file_path):

    #CSVが存在しなければ、Headerを追加する
    try:
        input_file = pd.read_csv(file_path,encoding='cp932')
    except:
        get_date_list.insert(0,"取得日")
        detail_url_list.insert(0,"詳細URL")
        seach_title_list.insert(0,"検索タイトル")
            
    #CSVに出力
    data = zip(get_date_list,detail_url_list,seach_title_list)
    with open(file_path,'a',errors='backslashreplace',encoding="SHIFT-JIS") as fout:
            writecsv = csv.writer(fout,lineterminator='\n')
            writecsv.writerows(data)

#item_listのアウトプット
def create_csv_item_list(file_path):
    
    #CSVが存在しなければ、Headerを追加する
    try:
        input_file = pd.read_csv(file_path,encoding='cp932')
    except:
        get_date_list.insert(0,"取得日")
        detail_url_list.insert(0,"詳細URL")
        seach_title_list.insert(0,"検索タイトル")
        shop_name_list.insert(0,"店舗名")
        first_janre_list.insert(0,"ジャンル1")
        second_janre_list.insert(0,"ジャンル2")
        third_janre_list.insert(0,"ジャンル3")
        four_janre_list.insert(0,"ジャンル4")
        evaluation_list.insert(0,"評価")
        prefectures_list.insert(0,"都道府県")
        street_adress_list.insert(0,"住所")
        tel_number_list.insert(0,"電話番号")
        budget_lunch_lower_list.insert(0,"予算_昼_下限")
        budget_lunch_upper_list.insert(0,"予算_昼_上限")
        budget_dinner_lower_list.insert(0,"予算_夜_下限")
        budget_dinner_upper_list.insert(0,"予算_夜_上限")

    #zipに一括化
    data = zip(
            get_date_list, #取得日 
            detail_url_list, #詳細URL
            seach_title_list, #検索タイトル
            shop_name_list, #店舗名
            first_janre_list, #ジャンル1
            second_janre_list, #ジャンル2
            third_janre_list, #ジャンル3
            four_janre_list, #ジャンル4
            evaluation_list, #評価
            prefectures_list, #都道府県
            street_adress_list, #住所
            tel_number_list, #電話番号
            budget_lunch_lower_list, #予算_昼_下限
            budget_lunch_upper_list, #予算_昼_上限
            budget_dinner_lower_list, #予算_夜_下限
            budget_dinner_upper_list, #予算_夜_上限
            )
    
    #CSVに出力
    with open(file_path,'a',errors='backslashreplace',encoding="SHIFT-JIS") as fout:
            writecsv = csv.writer(fout,lineterminator='\n')
            writecsv.writerows(data)

#URLを生成
def create_url_adress(page_number) ->str:
    
    #取得対象URL
    target_url = "https://tabelog.com/tokyo/A1303/A130301/rstLst/"
    
    marge_url = target_url + str(page_number) + "/"
    
    return marge_url


#URL_listのファイルpathを生成
def create_file_path(file_path,file_category) ->str:

    #ファイル名
    area_name = "shibuya"

    #CSVファイル名
    csv_file_name = file_path + date_time + "_" + "tabelog" + "_" + area_name + "_" + file_category + ".csv"
    
    return csv_file_name

def main():

    #今日の日付
    global date_time
    date_time = str(datetime.date.today())
    
    #待機時間
    global succses_wait_time
    global failure_wait_time
    succses_wait_time = 5 #取得成功後の待機時間
    failure_wait_time = 60 #取得失敗後の待機時間
    
    #現在のページ数を定義
    current_page_number = 1
    
    #URLを生成する
    target_url = create_url_adress(current_page_number)
    
    #ページ数を取得
    page_count = Get_data(target_url).page_count()
    
    #今回スクレイピングするリストを格納するfile_path
    file_path_url_list = create_file_path("../url_list/","url_list")
    
    #成果物（output）を格納するpath
    file_path_item_list = create_file_path("../output/","output")

    #取得日と全ページの詳細URLを取得
    for i in range(page_count):
        
        #URLを生成する
        target_url = create_url_adress(current_page_number)
        
        #url_listを取得
        create_url_list = Get_data(target_url).url_data()
        
        #CSVを生成
        create_csv = create_csv_url_list(file_path_url_list)
        
        print("{}ページ目のページ取得が完了しました。".format(current_page_number))
        
        #現ページ数を1ページ加算
        current_page_number += 1
        

    #inputするファイルを読み込み
    try:
        global csv_input_list
        csv_input_list = pd.read_csv(file_path_url_list,encoding='cp932')
    except:
        print("詳細URLリストがありません。")
        sys()

    #outputするファイルを読み込み。存在しない場合はcsv_output_list_last_rowのlengthを0にするためにnullにする。
    try:
        csv_output_list = pd.read_csv(file_path_item_list,encoding='cp932')
    except:
        csv_output_list = ""

    #求人詳細URLの最終行を取得
    csv_input_list_last_row = len(csv_input_list["詳細URL"])

    #項目リストの最終行を取得
    global csv_output_list_last_row
    csv_output_list_last_row = len(csv_output_list)

    ############################
    #各項目を取得して、CSVに格納
    ############################

    for i in range(csv_input_list_last_row):

        #各項目を取得
        Get_data(csv_input_list["詳細URL"][csv_output_list_last_row]).all_data()

        #CSVを格納
        create_csv_item_list(file_path_item_list)

        csv_output_list_last_row +=1

        #進捗をprintで出力
        print("{}件目の求人が完了しました。".format(csv_output_list_last_row))
    print("スクレイピングが完了しました")

if __name__ == "__main__":
    main()