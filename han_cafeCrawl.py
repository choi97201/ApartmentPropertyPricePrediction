from selenium import webdriver
import time
import pyperclip
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os


def login():
    driver.get('https://nid.naver.com/nidlogin.login')

    login_btn = driver.find_element_by_css_selector('#frmNIDLogin > fieldset > input')
    login_btn.click()

    tag_id = driver.find_element_by_name('id')
    tag_pw = driver.find_element_by_name('pw')
    tag_id.clear()

    tag_id.click()
    pyperclip.copy(ID)
    tag_id.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    tag_pw.click()
    pyperclip.copy(PW)
    tag_pw.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    driver.find_element_by_css_selector('#frmNIDLogin > fieldset > input').click()
    time.sleep(1)
    driver.refresh()

def cafe(code):
    # 로그인
    login()
    df = []
    url = 'https://cafe.naver.com/jaegebal?iframe_url=/ArticleList.nhn%3Fsearch.clubid=12730407%26search.menuid={}%26search.boardtype=L'.format(code)
    driver.get(url)
    # frame switch
    try:
        time.sleep(TIME_SLEEP)
        driver.switch_to.frame('cafe_main')
    except Exception:
        time.sleep(2)
        driver.switch_to.frame('cafe_main')

    page = 3
    first = True
    while True:
        try:
            date = driver.find_elements_by_css_selector('#main-area > div:nth-child(6) > table > tbody > tr > td.td_date')
            title = driver.find_elements_by_css_selector('#main-area > div:nth-child(6) > table > tbody > tr > td.td_article > div.board-list > div > a.article')
            for idx, t in enumerate(title):
                df.append([date[idx].text, t.text])
            try:
                tmp = date[0].text.split('.')
                if int(tmp[0]) < 2013:
                    if int(tmp[1]) < 5:
                        break
            except Exception as e:
                print(e.args)
                pass

            if first:
                if page < 12:
                    next = driver.find_elements_by_css_selector('#main-area > div.prev-next > a')
                    page += 1
                    print(next[page - 3].text)
                    next[page - 3].click()
                elif page == 12:
                    next = driver.find_element_by_css_selector('#main-area > div.prev-next > a.pgR')
                    page = 3
                    print(next.text)
                    next.click()
                    first = False
            else:
                if page < 13:
                    next = driver.find_elements_by_css_selector('#main-area > div.prev-next > a')
                    page += 1
                    print(next[page - 3].text)
                    next[page - 3].click()
                elif page == 13:
                    next = driver.find_element_by_css_selector('#main-area > div.prev-next > a.pgR')
                    page = 3
                    print(next.text)
                    next.click()

        except Exception as e:
            print(e.args)
            break
    df = pd.DataFrame(df)
    df.columns = ['Date', 'Title']
    df.to_csv(os.path.join('data', 'cafe', '{}.csv'.format(RegionDic[code])), encoding='utf-8', index=False)
    print('saved...')
    driver.quit()


DRIVER_PATH = 'D:/chromedriver.exe'
TIME_SLEEP = 0
ID = ''
PW = '@@'
RegionDic = {16 : '용산구', 27 : '마포구', 26 : '중구', 36 : '성동구', 45 : '동작구', 60 : '관악구',
                  43 : '광진구', 64 : '강남구', 65 : '서초구', 44 : '강동구', 62 : '송파구', 23 : '영등포구',
                  184 : '금천구', 58 : '양천구', 63 : '강서구', 66 : '구로구', 31 : '서대문구', 47 : '은평구',
                  54 : '종로구', 61 : '강북구', 50 : '성북구', 22 : '동대문구', 87 : '도봉구', 69 : '중랑구',
                  159 : '노원구'}
codeArr = list(RegionDic.keys())
for code in codeArr:
    driver = webdriver.Chrome(DRIVER_PATH)
    print(RegionDic[code])
    try:
        cafe(code)
    except Exception as e:
        pass