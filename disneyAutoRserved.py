from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import urllib.request
import webbrowser
import requests
import time
import sys
import datetime
import signal
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

#ラインへ通知を送る関数
def line_broadcast_full(mess):
    url = "https://api.line.me/v2/bot/message/broadcast"
    token = '[your channel accessToken]'
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json"
    }
    res = requests.post(url, headers=headers, json={"messages":[{"type" : "text","text":mess}]})
    print(res)
def line_broadcast_empty(mess):
    url = "https://api.line.me/v2/bot/message/broadcast"
    token = '[your channel accessToken]'
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json"
    }
    res = requests.post(url, headers=headers, json={"messages":[{"type" : "text","text":mess}]})
    print(res)

def initOption():
    options = Options()
    # options.binary_location = '/usr/bin/google-chrome'
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--lang=ja-JP')
    options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36') 
    options.add_argument('--blink-settings=imagesEnabled=false')

    driver = webdriver.Chrome(executable_path=resource_path('./driver/chromedriver.exe'), options=options)
    driver.implicitly_wait(30)
    # ホテルページに遷移する。
    url = 'https://reserve.tokyodisneyresort.jp/sp/hotel/list/?showWay=&roomsNum=1&adultNum=2&childNum=0&stayingDays=2&useDate=20220617&cpListStr=&childAgeBedInform=&searchHotelCD=TSH&searchHotelDiv=&hotelName=&searchHotelName=&searchLayer=&searchRoomName=&hotelSearchDetail=true&detailOpenFlg=0&checkPointStr=&hotelChangeFlg=false&removeSessionFlg=true&returnFlg=false&hotelShowFlg=&displayType=data-hotel&reservationStatus=1'
    driver.get(url)

    try:
        all_images = []
        time.sleep(20)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        indexEcRoomTitle = 0
        for ecRoomTitle in soup.find_all('div', class_='ecRoomTitleBar'):
            if indexEcRoomTitle == 17 or indexEcRoomTitle == 18 or indexEcRoomTitle == 19 or indexEcRoomTitle == 20:
                ecRoomFull = ecRoomTitle.find('span').get_text()
                if ecRoomFull== '円':
                    title = ecRoomTitle.find('h1').get_text().strip()
                    lineMessage = '部屋名：' + title + '\n' + '空き状況：' + "空いています"
                    print(lineMessage)
                else :
                    title = ecRoomTitle.find('h1').get_text().strip()
                    ecRoomFull = ecRoomTitle.find('span').get_text()
                    lineMessage = '部屋名：' + title + '\n' + '空き状況：' + ecRoomFull
                    print(lineMessage)
                # line_broadcast_full(lineMessage)
            if indexEcRoomTitle == 21:
                ecRoomFull = ecRoomTitle.find('span').get_text()
                if ecRoomFull== '円':
                    title = ecRoomTitle.find('h1').get_text().strip()
                    lineMessage = '【空き部屋有！】' + '\n' + '部屋名：' + title + '\n' + '上記部屋が空き部屋となっているため、以下リンクから予約してください。' + '\n' + 'https://reserve.tokyodisneyresort.jp/sp/hotel/list/?showWay=&roomsNum=1&adultNum=2&childNum=0&stayingDays=2&useDate=20220617&cpListStr=&childAgeBedInform=&searchHotelCD=TSH&searchHotelDiv=&hotelName=&searchHotelName=&searchLayer=&searchRoomName=&hotelSearchDetail=true&detailOpenFlg=0&checkPointStr=&hotelChangeFlg=false&removeSessionFlg=true&returnFlg=false&hotelShowFlg=&displayType=data-hotel&reservationStatus=1'
                    print(lineMessage)
                    line_broadcast_empty(lineMessage)
            indexEcRoomTitle += 1
    except:
        print("タイムアウトしました")  
    finally:
        html = driver.page_source

initOption()

