# -*- coding: utf-8 -*-
from time import sleep
from urllib.request import urlopen
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.support import expected_conditions as EC
import lxml
import mysql.connector

# いいねをする際の初期設定
print("スクロールする回数を入力してください。")
scroll_num = int(input())

# ログイン、URLを開く
current_path = os.getcwd()
driver_path = current_path + "/chromedriver"
driver = webdriver.Chrome(executable_path=driver_path)
login_url = "https://twitter.com/login"
driver.get(login_url)
username = driver.find_element_by_css_selector(
    '#page-container > div > div.signin-wrapper > form > fieldset > div:nth-child(2) > input')
password = driver.find_element_by_css_selector(
    '#page-container > div > div.signin-wrapper > form > fieldset > div:nth-child(3) > input')
username.send_keys("ユーザーネームをここに入れます")
password.send_keys("パスワードを入れます")
password.send_keys(keys.ENTER)
driver.get("https://twitter.com/AI_Academy_JP/following")


# scroll関数
def scroll(num):
    for i in range(num):
        print(str(i + 1) + "回目のスクロールをしました。")
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)


# スクロール実行
scroll(scroll_num)

# ツイートのリスト作成
html_source = driver.page_source
soup = BeautifulSoup(html_source, "lxml")
username = []
un_username = []
user = soup.find_all(class_="Grid-cell u-size1of2 u-lg-size1of3 u-mb10")
user_len = len(user)
print("片思いチェックをするユーザー数は" + str(user_len) + "です。")
for ul in  range(user_len) :
    for u in user :
        id = u.div.get("data-item-id")
        id = str(id)
        user_name = u.select_one("#stream-item-user-{} > div > div > div.ProfileCard-userFields > span > a > span > b".format(id)).string
        try :
            if  u.find(class_="FollowStatus").string :
                username.append(user_name)
        except :
                un_username.append(user_name)
usernames = list (set(username))
un_usernames = list (set(un_username))
try :
    usernames.remove("Ai_Academy_JP")
    un_usernames.remove("Ai_Academy_JP")
except :
    pass
print("両思いユーザー数は" + str(len(usernames)) + "で、ユーザー名は以下です。")
print(usernames)
print("片思いユーザー数は" + str(len(un_usernames)) + "で、ユーザー名は以下です。")
print(un_usernames)

cnx = mysql.connector.connect(user='root', password='', host='localhost', database='twitter', charset='utf8')
cur = cnx.cursor()
stmt = ("truncate table follow_history")
cur.execute(stmt)
cnx.commit
for u in usernames :
    stmt = ("INSERT INTO follow_history "
               "(name, follow) "
               "VALUES (%s, %s)")
    data = (u, 1)
    cur.execute(stmt, data)
for u in un_usernames :
    stmt = ("INSERT INTO follow_history "
               "(name, follow) "
               "VALUES (%s, %s)")
    data = (u, 0)
    cur.execute(stmt, data)
cnx.commit()

cur.close()
cnx.close()
