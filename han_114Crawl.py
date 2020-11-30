from selenium import webdriver
import pandas as pd
import time
import os

dataDf = []
errorDf = []

def crawling(i, j, n):
    try:
        driver = webdriver.Chrome("D:/chromedriver.exe")
        url = "https://www.r114.com/?_c=memul&_m=p10&direct=A"
        driver.get(url)
        try:
            btnAdress = driver.find_element_by_css_selector('#addressTitle > a')
            btnAdress.click()
        except Exception as e:
            print(e.args)
            time.sleep(1)
            btnAdress = driver.find_element_by_css_selector('#addressTitle > a')
            btnAdress.click()
        # 시
        time.sleep(2)
        btnList = driver.find_elements_by_css_selector('#msrch_wrap_selectarea_Addr > li')
        btnList[0].click()
        # 구
        time.sleep(2)
        btnList = driver.find_elements_by_css_selector('#msrch_wrap_selectarea_Addr > li')
        btnList[i].click()
        # 동
        time.sleep(2)
        btnList = driver.find_elements_by_css_selector('#msrch_wrap_selectarea_Addr > li')
        btnList[j].click()
        # 바로가기
        time.sleep(2)
        btnList = driver.find_element_by_css_selector('#msrch_wrap_selectarea_Addr > li:nth-child(1) > a')
        btnList.click()
        # 아파트
        try:
            time.sleep(5)
            btnList = driver.find_elements_by_css_selector('ul.map_info_list > li')
            btnList[0].click()
        except:
            driver.refresh()
            time.sleep(10)
            btnList = driver.find_elements_by_css_selector('ul.map_info_list > li')
            btnList[0].click()
        # 아파트개수
        aptLen = len(btnList)
        # 단지정보
        try:
            time.sleep(3)
            btnList = driver.find_elements_by_css_selector('.contents_wrap > ul > li > a')
            btnList[3].send_keys('\n')
        except Exception as e:
            time.sleep(10)
            btnList = driver.find_element_by_css_selector(
                '#body_layout > div > div.contents_wrap > ul.list_tab3.clearfix.tabMenu.n4 > li:nth-child(4) > a')
            btnList.click()
        x = n
        # 아파트다돌기
        while x < aptLen:
            tmp = []
            try:
                time.sleep(2)
                btnList = driver.find_elements_by_css_selector('ul.map_info_list > li')
                btnList[x].click()
                print(btnList[x].text)
                tmp.append(btnList[x].text)
            except:
                try:
                    time.sleep(10)
                    btnList = driver.find_elements_by_css_selector('ul.map_info_list > li')
                    btnList[x].click()
                    print(btnList[x].text)
                    tmp.append(btnList[x].text)
                except:
                    driver.refresh()
                    time.sleep(10)
                    btnList = driver.find_elements_by_css_selector('ul.map_info_list > li')
                    btnList[x].click()
                    print(btnList[x].text)
                    tmp.append(btnList[x].text)
                    try:
                        time.sleep(3)
                        btnList = driver.find_elements_by_css_selector('.contents_wrap > ul > li > a')
                        btnList[3].send_keys('\n')
                    except Exception as e:
                        time.sleep(10)
                        btnList = driver.find_element_by_css_selector(
                            '#body_layout > div > div.contents_wrap > ul.list_tab3.clearfix.tabMenu.n4 > li:nth-child(4) > a')
                        btnList.click()
            # 주소           
            try:
                time.sleep(2)
                address = driver.find_element_by_css_selector('#spnAddr1')
            except:
                try:
                    time.sleep(2)
                    address = driver.find_element_by_css_selector('#spnAddr1')
                except:
                    x += 1
                    continue
            print(address.text)
            tmp.append(address.text)

            # 시공사
            # try:
            #     time.sleep(2)
            #     company = driver.find_element_by_css_selector('#divCompexTab > table > tbody > tr > td > div:nth-child(3) > ul > li > span.spndetail')
            # except:
            #     time.sleep(2)
            #     company = driver.find_element_by_css_selector('#divCompexTab > table > tbody > tr > td > div:nth-child(3) > ul > li > span.spndetail')
            # print(company.text)
            # tmp.append(company.text)

            # 학군
            try:
                school = driver.find_element_by_css_selector(
                    '#body_layout > div > div.contents_wrap > div.setAreaDetail > div:nth-child(32) > ul.list_school > li:nth-child(1) > div > strong')
            except:
                try:
                    school = driver.find_element_by_css_selector(
                        '#body_layout > div > div.contents_wrap > div.setAreaDetail > div:nth-child(31) > ul.list_school > li:nth-child(1) > div > strong')
                except:
                    try:
                        school = driver.find_element_by_css_selector(
                            '#body_layout > div > div.contents_wrap > div.setAreaDetail > div:nth-child(30) > ul.list_school > li:nth-child(1) > div > strong')
                    except:
                        try:
                            school = driver.find_element_by_css_selector(
                                '#body_layout > div > div.contents_wrap > div.setAreaDetail > div:nth-child(29) > ul.list_school > li:nth-child(1) > div > strong')
                        except:
                            school = driver.find_element_by_css_selector(
                                '#body_layout > div > div.contents_wrap > div.setAreaDetail > div:nth-child(28) > ul.list_school > li:nth-child(1) > div > strong')
            print(school.text)
            tmp.append(school.text)
            try:
                school2 = driver.find_element_by_css_selector(
                    '#body_layout > div > div.contents_wrap > div.setAreaDetail > div:nth-child(32) > ul.list_school > li:nth-child(1) > span')
            except:
                try:
                    school2 = driver.find_element_by_css_selector(
                        '#body_layout > div > div.contents_wrap > div.setAreaDetail > div:nth-child(31) > ul.list_school > li:nth-child(1) > span')
                except:
                    try:
                        school2 = driver.find_element_by_css_selector(
                            '#body_layout > div > div.contents_wrap > div.setAreaDetail > div:nth-child(30) > ul.list_school > li:nth-child(1) > span')
                    except:
                        try:
                            school2 = driver.find_element_by_css_selector(
                                '#body_layout > div > div.contents_wrap > div.setAreaDetail > div:nth-child(29) > ul.list_school > li:nth-child(1) > span')
                        except:
                            school2 = driver.find_element_by_css_selector(
                                '#body_layout > div > div.contents_wrap > div.setAreaDetail > div:nth-child(28) > ul.list_school > li:nth-child(1) > span')
            print(school2.text)
            tmp.append(school2.text)
            
            # 지하철
            try:
                subway = driver.find_element_by_css_selector('#divSubway > ul')
                print(subway.text)
                tmp.append(subway.text)
            except:
                print('no subway')
                tmp.append('no subway')

            dataDf.append(tmp)
            x += 1

    except Exception as e:
        print(e.args)
        try:
            errorDf.append([i, j, x, e.args])
        except:
            errorDf.append([i, j, n, e.args])
    driver.quit()


path = os.path.join('D:/han_project01/project/data/행정동.xlsx')

dong = pd.read_excel(path)
dongArr = list(dong['동수'])

for i in range(21, 26):
    for j in range(5):
        dataDf = []
        errorDf = []
        crawling(i, j, 0)
        if dataDf:
            path = os.path.join('D:/han_project01/project/data/아파트2.csv')
            pd.DataFrame(dataDf).to_csv(path, mode='a', encoding='euc-kr', index=False, header=False)
        if errorDf:
            path = os.path.join('D:/han_project01/project/data/error.csv')
            pd.DataFrame(errorDf).to_csv(path, mode='a', encoding='euc-kr', index=False, header=False)

# path = os.path.join('D:/han_project01/project/data/error.csv')
# errorDf_ = pd.read_csv(path, names=['i', 'j', 'n'], encoding='utf-8')
# for idx in range(errorDf_.shape[0]):
#     dataDf = []
#     errorDf = []
#     crawling(errorDf_['i'][idx], errorDf_['j'][idx], errorDf_['n'][idx])
#     if dataDf:
#         path = os.path.join('D:/han_project01/project/data/아파트2.csv')
#         pd.DataFrame(dataDf).to_csv(path, mode='a', encoding='euc-kr', index=False, header=False)
#     if errorDf:
#         path = os.path.join('D:/han_project01/project/data/error2.csv')
#         pd.DataFrame(errorDf).to_csv(path, mode='a', encoding='utf-8', index=False, header=False)