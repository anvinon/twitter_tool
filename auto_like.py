# -*- coding: utf-8 -*-
from time import sleep
from urllib.request import urlopen
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.support import expected_conditions as EC
import lxml

# いいねをする際の初期設定
print("スクロールする回数を入力してください。")
scroll_num = int(input())
print("Twitter内をキーワード検索かけたときのURLを入力してください")
follow_url = str(input())
opened_url = urlopen(follow_url)

# ログイン、URLを開く
current_path = os.getcwd()
driver_path = current_path + "/chromedriver"
driver = webdriver.Chrome(executable_path=driver_path)
login_url = "https://twitter.com/login"
driver.get(login_url)
username = driver.find_element_by_css_selector('#page-container > div > div.signin-wrapper > form > fieldset > div:nth-child(2) > input')
password = driver.find_element_by_css_selector('#page-container > div > div.signin-wrapper > form > fieldset > div:nth-child(3) > input')
username.send_keys("ユーザーネームをここに入れます")
password.send_keys("パスワードをここに入れます")
password.send_keys(keys.ENTER)
driver.get(follow_url)


# scroll関数
def scroll(num):
    for i in range(num):
        print(str(i + 1) + "周完了!画面をスクロールするよ")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)


# スクロール実行
scroll(scroll_num)

# ツイートのリスト作成
html_source = driver.page_source
soup = BeautifulSoup(html_source, "lxml")
tweet_ids = []
tag = soup.find_all(class_="stream-item")
for t in tag :
    try :
        tweet_id = t.get("data-item-id")
        tweet_ids.append(tweet_id)
    except :
        pass
print("ツイートをリストに追加終了")
print(str(len(tweet_ids)) + "のツイートをリストに追加")

# いいね処理
tweet_count = 0
for t in tweet_ids :
    try :
        tweet_count = tweet_count + 1
        driver.find_element_by_css_selector('#stream-item-tweet-{id} > div > div.content > div.stream-item-footer > div.ProfileTweet-actionList.js-actions > div.ProfileTweet-action.ProfileTweet-action--favorite.js-toggleState > button.ProfileTweet-actionButton.js-actionButton.js-actionFavorite > div > div'.format(id=t)).click()
    except Exception as e  :
        print("エラーが出ました。エラーが出た要素は以下。", e)
        print(tweet_count)
    sleep(1)

print("終了")
