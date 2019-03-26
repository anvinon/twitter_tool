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
print("Twitter内をキーワード検索にかけたときのURLを入力してください")
follow_url = str(input())
opened_url = urlopen(follow_url)

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
password.send_keys("パスワードをここに入れます")
password.send_keys(keys.ENTER)
driver.get(follow_url)

# スクロール
for i in range(scroll_num):
    print(str(i + 1) + "回目のスクロールをしました。")
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)

# フォローユーザー候補のIDのリスト作成
html_source = driver.page_source
soup = BeautifulSoup(html_source, "lxml")
username = []
span = soup.find_all("span", class_="username u-dir u-textTruncate")
for s in span :
    user = s.b.string
    username.append(user)
print("フォローユーザー候補のIDは" + str(len(username)) + "です。")

# 片思いだったのでフォロー解除をしたアカウントを、リストから削除
cnx = mysql.connector.connect(user='root', password='', host='localhost', database='twitter', charset='utf8')
cur = cnx.cursor()
stmt = ("SELECT name FROM follow_history WHERE follow=%s")
data = 0
cur.execute(stmt, (data,))
un_user = cur.fetchall()
username = list (set(username))
cnt = 0
uuser_list = []
for u in un_user :
    u = u[0]
    uuser_list.append(u)
for u in uuser_list :
    try :
        username.remove(u)
        print(u + "は片思いアカウントだったので再度フォロー処理をしません。")
    except ValueError :
        cnt += 1
print("このキーワードをツイートしているユーザーのリストの数は" + str(len(username)) + "で、ユーザー名は以下です。")
print(username)

# フォロー実行
for u in username :
    driver.get("https://twitter.com/" + u)
    print(u + "のページを開きました。")
    sleep(1)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "lxml")
    try :
        btn_message = soup.select_one("#page-container > div.ProfileCanopy.ProfileCanopy--withNav.ProfileCanopy--large.js-variableHeightTopBar > div > div.ProfileCanopy-navBar.u-boxShadow > div > div > div.Grid-cell.u-size2of3.u-lg-size3of4 > div > div > ul > li.ProfileNav-item.ProfileNav-item--userActions.u-floatRight.u-textRight.with-rightCaret > div > div > span.user-actions-follow-button.js-follow-btn.follow-button > button.EdgeButton.EdgeButton--secondary.EdgeButton--medium.button-text.follow-text ").span.string
    except :
        try :
            btn_message = soup.select_one("#page-container > div.ProfileCanopy.ProfileCanopy--withNav.js-variableHeightTopBar > div > div.ProfileCanopy-navBar.u-boxShadow > div > div > div.Grid-cell.u-size2of3.u-lg-size3of4 > div > div > ul > li.ProfileNav-item.ProfileNav-item--userActions.u-floatRight.u-textRight.with-rightCaret > div > div > span.user-actions-follow-button.js-follow-btn.follow-button > button.EdgeButton.EdgeButton--secondary.EdgeButton--medium.button-text.follow-text ").span.string
        except :
            btn_message = ""
    if btn_message == "フォローする" :
        try :
            driver.find_element_by_css_selector('#page-container > div.ProfileCanopy.ProfileCanopy--withNav.ProfileCanopy--large.js-variableHeightTopBar > div > div.ProfileCanopy-navBar.u-boxShadow > div > div > div.Grid-cell.u-size2of3.u-lg-size3of4 > div > div > ul > li.ProfileNav-item.ProfileNav-item--userActions.u-floatRight.u-textRight.with-rightCaret > div > div > span.user-actions-follow-button.js-follow-btn.follow-button > button.EdgeButton.EdgeButton--secondary.EdgeButton--medium.button-text.follow-text > span:nth-child(1)').click()
        except :
            try :
                driver.find_element_by_css_selector('#page-container > div.ProfileCanopy.ProfileCanopy--withNav.js-variableHeightTopBar > div > div.ProfileCanopy-navBar.u-boxShadow > div > div > div.Grid-cell.u-size2of3.u-lg-size3of4 > div > div > ul > li.ProfileNav-item.ProfileNav-item--userActions.u-floatRight.u-textRight.with-rightCaret > div > div > span.user-actions-follow-button.js-follow-btn.follow-button > button.EdgeButton.EdgeButton--secondary.EdgeButton--medium.button-text.follow-text > span:nth-child(1)').click()
            except :
                pass
        finally :
            print(u + "をフォローしました。")
    else :
        print(u + "をフォローしませんでした。")

sleep(1)
print("フォロー完了しました。")
