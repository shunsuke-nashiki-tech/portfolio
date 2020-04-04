import urllib, requests, regex, csv, re, math, time, datetime, random
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

####################################
#変数を定義する
####################################

#スクレイピング後の待機時間
wait_time_after_scrayping = random.randint(5, 10)

#市名
city_name = "ginza"

#取得対象URL
target_get_url = "https://tabelog.com/tokyo/A1301/A130101/"

#実行日
run_time = str(datetime.date.today())

#CSVファイル名
get_csv_file = "../csv/tabelog" + city_name + run_time + ".csv"

#ページ数の初期値
page_number = 1

#格納用CSVを生成
def Output_csv():

    #CSVが存在しなければ、ヘッダーを作成して格納
    try:
        read_file = pd.read_csv(get_csv_file,encoding='cp932')
    except:
        details_url_list = []


        details_url_list.append("URL")
        evaluation_list.append("評価")
        shop_name_list.append("最寄り駅")
        
        data = zip(details_url_list)
        with open(get_csv_file,'a',errors='backslashreplace',encoding="SHIFT-JIS") as fout:
            writecsv = csv.writer(fout,lineterminator='\n')
            writecsv.writerows(data)

#件数を取得してページ数を算出
def Run_page_count():

    #Beautifulsoupで要素を取得
    html = urllib.request.urlopen(target_get_url)
    soup = BeautifulSoup(html, 'lxml')
    time.sleep(wait_time_after_scrayping)

    #全件数を取得して、1ページの要素数（20件）で除算
    for table in soup.findAll(class_="list-condition__count"):
        page_count = re.sub(",","",table.text)
        page_count = math.ceil(int(page_count) / 20)

    return page_count

#要素数をインスタンス化
page_count = Run_page_count()

print(page_count)





    




