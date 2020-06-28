import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


data = pd.read_excel('data.xls')
company = data['기업명']

company_input = input("기업명을 입력하세요")
company_input = str(company_input)
company_input = company_input.upper()

count = 0
company_spec = 0
for i in company:
    count += 1
    if i == company_input:
        company_spec = count

stockcodelist = []

for i in data['종목코드']:
    if len(str(i)) == 1:
        i = '00000' + str(i)
        stockcodelist.append(i)
    elif len(str(i)) == 2:
        i = '0000' + str(i)
        stockcodelist.append(i)
    elif len(str(i)) == 3:
        i = '000' + str(i)
        stockcodelist.append(i)
    elif len(str(i)) == 4:
        i = '00' + str(i)
        stockcodelist.append(i)
    elif len(str(i)) == 5:
        i = '0' + str(i)
        stockcodelist.append(i)
    elif len(str(i)) == 6:
        i = str(i)
        stockcodelist.append(i)
    else:
        print("none")

code = stockcodelist[(company_spec) - 1]

code = str(code)
url = "https://finance.naver.com/item/main.nhn?code=" + code
result = requests.get(url)
bs_obj = BeautifulSoup(result.content, "html.parser")
 

    # close 종가(전일)
td_first = bs_obj.find("td", {"class": "first"})  # 태그 td, 속성값 first 찾기
blind = td_first.find("span", {"class": "blind"})  # 태그 span, 속성값 blind 찾기
close = blind.text
 
# high 고가
table = bs_obj.find("table", {"class": "no_info"})  # 태그 table, 속성값 no_info 찾기
trs = table.find_all("tr")  # tr을 list로 []
first_tr = trs[0]  # 첫 번째 tr 지정
tds = first_tr.find_all("td")  # 첫 번째 tr 안에서 td를 list로
second_tds = tds[1]  # 두 번째 td 지정
high = second_tds.find("span", {"class": "blind"}).text
 
# open 시가
second_tr = trs[1]  # 두 번째 tr 지정
tds_second_tr = second_tr.find_all("td")  # 두 번째 tr 안에서 td를 list로
first_td_in_second_tr = tds_second_tr[0]  # 첫 번째 td 지정
open = first_td_in_second_tr.find("span", {"class": "blind"}).text
 
# low 저가
second_td_in_second_tr = tds_second_tr[1]  # 두 번째 td 지정
low = second_td_in_second_tr.find("span", {"class": "blind"}).text

no_today = bs_obj.find("p", {"class": "no_today"})
now_price = no_today.find("span", {"class": "blind"}).text


now = datetime.now()
month = now.month
date = now.day
hour = now.hour
minute = now.minute

open_int = open.replace(",", "")
open_int = int(open_int)
now_int = now_price.replace(",", "")
now_int = int(now_int)

difference = open_int - now_int
if difference < 0:
    dif = "상승"
else:
    dif = "하락"
difference = abs(difference)

print(f"{month}월 {date}일 {hour}시 {minute}분 현재 {company_input}의 주가는 {now_price}원으로 {open} 대비 {difference}원 {dif}했다.")
