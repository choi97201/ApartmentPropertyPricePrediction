import os

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from han_utils import dateChange

def loadSalesData(dir):
    print('Load sales data...')
    path = os.path.join(dir, 'data', 'apartment', 'all.csv')
    if os.path.isfile(path):
        df = pd.read_csv(path, encoding='utf-8')
    else:
        pathChanged = os.path.join(dir, 'data', 'apartment')
        fileList = os.listdir(pathChanged)
        csvFiles = []

        for f in fileList:
            if '.csv' in f:
                df = pd.read_csv(os.path.join(pathChanged, f), encoding='utf-8')
                print(df.head())
                csvFiles.append(df)
        df = pd.concat(csvFiles)
        # 주택매매가격지수 데이터 2012년 5월 7일부터
        df = df[(df['계약일'].astype('int') >= 20120507)].reset_index(drop=True)
        df.to_csv(path, encoding='utf-8', index=False)
    return df[['시군구', '번지', '전용면적(㎡)', '계약일', '거래금액(만원)', '층', '단지명', '건축년도']]

def loadInnerData(dir):
    print('Load inner data...')
    path = os.path.join(dir, 'data', '아파트2.csv')
    df = pd.read_csv(path, encoding='euc-kr')
    df.columns = ['단지명2', '주소', '학교', '학군', '역']
    df = df.drop(df[df['단지명2'] == '0'].index).reset_index(drop=True)
    df = df[['단지명2', '주소', '학군', '역']]
    arr = []
    for i in range(df.shape[0]):
        tmp = df['단지명2'][i]
        for idx, s in enumerate(tmp):
            if tmp[-(idx + 1)] == '(':
                arr.append(tmp[:-(idx + 1)])
                break
    df['단지명'] = arr
    df = df[['주소', '단지명', '학군', '역']]
    arr = []
    for i in range(df.shape[0]):
        tmp = df['주소'][i]
        if '도로명주소' in tmp:
            arr.append(tmp[:-6])
        else:
            arr.append(tmp)
    df['주소'] = arr
    df1 = df[df['역'] != 'no subway'].reset_index(drop=True)
    df2 = df[df['역'] == 'no subway'].reset_index(drop=True)
    arr = []
    for i in range(df1.shape[0]):
        tmp2 = df1['역'][i]
        sub = tmp2.split('\n')
        words = []
        for j in sub:
            for idx, s in enumerate(j):
                if j[-(idx + 1)] == '(':
                    words.append(j[:-(idx + 4)])
                    break

        subTmp = []
        for word in words:
            for idx, s in enumerate(word):
                if word[-(idx + 1)] == ' ':
                    if int(word[-(idx):]) == 900:
                        subTmp.append(14)
                    elif int(word[-(idx):]) == 245:
                        subTmp.append(4)
                    elif int(word[-(idx):]) == 100:
                        subTmp.append(2)
                    else:
                        subTmp.append(int(word[-(idx):]))
                    break
        arr.append(np.min(subTmp))
    df1['역'] = arr
    df = pd.concat([df1, df2]).reset_index(drop=True)
    arr = []
    for i in range(df.shape[0]):
        arr.append(int(df['학군'][i][2:-1]))
    df['학군'] = arr
    df = df.drop(df[df['학군'] == -1].index)
    df = df.drop_duplicates(['주소']).reset_index(drop=True)

    arr1 = []
    arr2 = []
    for i in range(df.shape[0]):
        separator = ' '
        arr1.append(separator.join(df['주소'][i].split(' ')[:-1]))
        arr2.append(df['주소'][i].split(' ')[-1])
    df['시군구'] = arr1
    df['번지'] = arr2
    return df[['시군구', '번지', '주소', '학군', '역']]

def loadInnerData2(dir):
    print('Load inner data2...')
    path = os.path.join(dir, 'data', 'apartment2.csv')
    df = pd.read_csv(path, encoding='ANSI')
    df.rename(columns={'층수': '총층수'}, inplace=True)
    arr1 = []
    arr2 = []
    for i in range(df.shape[0]):
        tmp = df['주소'][i].split(' ')
        arr1.append('{} {} {}'.format(tmp[0], tmp[1], tmp[2]))
        arr2.append(tmp[3])
    df['시군구'] = arr1
    df['번지'] = arr2
    return df

def loadCompanyData(dir):
    csvFiles = []
    for i in range(2014, 2021):
        path = os.path.join(dir, 'data', 'company', '{}.xlsx'.format(i))
        df = pd.read_excel(path, encoding='utf-8')
        df['년도'] = [i] * df.shape[0]
        df['브랜드인지도'] = [1] * df.shape[0]
        df = df.drop(['순위'], axis=1).reset_index(drop=True)
        df.columns = ['시공사', '년도', '브랜드인지도']
        df = df[:10]
        df = df.append(pd.DataFrame([['대한주택공사', i, 1]], columns=['시공사', '년도', '브랜드인지도']))
        csvFiles.append(df)

    df = pd.concat(csvFiles)
    return df

def loadDongData(dir, dong):
    print('Load {} data...'.format(dong))
    path = os.path.join(dir, 'data', 'dong', '{}.csv'.format(dong))
    df = pd.read_csv(path, encoding='utf-8')
    nameArr = df['단지명']
    newArr = []
    for n in nameArr:
        if '(' in n:
            for idx, s in enumerate(n):
                if n[-(idx + 1)] == '(':
                    newArr.append(n[:-(idx + 1)])
                    break
        else:
            newArr.append(n)
    df['단지명'] = newArr
    df = df.drop(['선호도'], axis=1)
    arr = []
    for i in range(df.shape[0]):
        arr.append(str(df['계약일'][i])[:4])
    df['년도'] = arr

    nameArr = df['시공사']
    newArr = []
    for n in nameArr:
        try:
            if '외' in n:
                for idx, s in enumerate(n):
                    if n[-(idx + 1)] == '외':
                        newArr.append(n[:-(idx + 1)])
                        break
            else:
                newArr.append(n)
        except:
            newArr.append(n)
    df['시공사'] = newArr

    nameArr = df['시공사']
    newArr = []
    for n in nameArr:
        try:
            if ',' in n:
                for idx, s in enumerate(n):
                    if n[-(idx + 1)] == ',':
                        newArr.append(n[:-(idx + 1)])
                        break
            else:
                newArr.append(n)
        except:
            newArr.append(n)
    df['시공사'] = newArr

    print('preprecess dong data...')
    cafeDf = loadCafeData(dir, dong.split(' ')[1])
    nameArr = np.unique(df['단지명'])
    newDf = []
    for year in range(2012, 2021):
        tmp = cafeDf[cafeDf['Year'] == str(year)].reset_index(drop=True)
        words = []
        for i in range(tmp.shape[0]):
            for n in nameArr:
                if n in tmp['Title'][i]:
                    words.append(n)
        try:
            tmpDf = pd.DataFrame(words).reset_index(drop=True)
            tmpDf.columns = ['단지명']
            tmpDf = pd.DataFrame(tmpDf['단지명'].value_counts()).reset_index()
            tmpDf.columns = ['단지명', '선호도']
            tmpDf['년도'] = [str(year)] * tmpDf.shape[0]
            newDf.append(tmpDf)
        except:
            pass
    newDf = pd.concat(newDf)
    newDf = pd.DataFrame.merge(df, newDf, on=['단지명', '년도'], how='outer')
    newDf = newDf.fillna(0)
    newDf = newDf.drop(newDf[newDf['시군구'] == 0].index).reset_index(drop=True)
    df = newDf
    arr1 = []
    arr2 = []
    arr3 = []
    for i in range(df.shape[0]):
        if df['역'][i] == 'no subway':
            arr1.append(0)
            arr2.append(0)
            arr3.append(1)
        else:
            if int(df['역'][i]) <= 5:
                arr1.append(1)
                arr2.append(0)
                arr3.append(0)
            elif int(df['역'][i]) > 5 and int(df['역'][i]) <= 10:
                arr1.append(0)
                arr2.append(1)
                arr3.append(0)
            else:
                arr1.append(0)
                arr2.append(0)
                arr3.append(1)
    df['근접역세권'] = arr1
    df['간접역세권'] = arr2
    df['비역세권'] = arr3
    arr = []
    for i in range(df.shape[0]):
        tmp = df['거래금액(만원)'][i]
        tmp2 = int(tmp.replace(",", ""))
        arr.append(tmp2)
    df['거래금액(만원)'] = arr

    companyDf = loadCompanyData(dir)
    companyDf['년도'] = companyDf['년도'].astype('str')
    df = pd.DataFrame.merge(df, companyDf, on=['시공사', '년도'], how='outer').fillna(0)
    df = df.drop(df[df['시군구'] == 0].index)

    selectedVar = ['전용면적(㎡)', '거래금액(만원)', '층', '건축년도', '학군', '총층수', '동수', '선호도']
    newDf = df[selectedVar]

    scaler = MinMaxScaler()
    newDf = pd.DataFrame(scaler.fit_transform(newDf))
    newDf.columns = selectedVar
    newDf[['주간아파트규모별매매가격지수', '근접역세권', '간접역세권', '비역세권', '브랜드인지도']] = df[['주간아파트규모별매매가격지수', '근접역세권', '간접역세권', '비역세권','브랜드인지도']]

    return df, newDf

def loadPreDongData(dir, dong):
    print('Load {} preprocessed data...'.format(dong))
    path = os.path.join(dir, 'data', 'preprocessedDong', '{}.csv'.format(dong))
    df = pd.read_csv(path, encoding='utf-8')
    return df

def loadPricePointData(dir, gu, size):
    path = os.path.join(dir, 'data', 'price', '{}_{}.csv'.format(gu, size))
    df = pd.read_csv(path, encoding='utf-8')
    scaler = MinMaxScaler()
    df[df.columns[1:]] = pd.DataFrame(scaler.fit_transform(df[df.columns[1:]]))
    return df

def loadCafeData(dir, gu):
    print('Load {} cafe data...'.format(gu))
    path = os.path.join(dir, 'data', 'cafe', '{}.csv'.format(gu))
    df = pd.read_csv(path, encoding='utf-8')
    arr = []
    for i in range(df.shape[0]):
        arr.append(df['Date'][i][:4])
    df['Year'] = arr
    df
    return df

def preprocessPricePointData(dir):
    data = {}
    regionDict = {}
    path = os.path.join(dir, 'data', 'week')
    df = pd.read_csv(os.path.join(path, '주간아파트매매가격지수.csv'))
    for idx in range(df.shape[0]):
        regionDict[df['지역'][idx]] = df['지역2'][idx]
    path = os.path.join(dir, 'data', 'week')
    fileList = os.listdir(path)
    data['SalesData'] = loadSalesData(dir)
    data['DongData'] = pd.DataFrame(data['SalesData']['시군구'].value_counts()).reset_index()
    data['DongData'].columns = ['시군구', '수']
    data['DongData'] = data['DongData'][data['DongData']['수'] >= 100].reset_index(drop=True)
    guArr = []
    for i in range(data['DongData'].shape[0]):
        guArr.append(data['DongData']['시군구'][i].split(' ')[1])
    for r in guArr:
        sizes = ['40㎡초과 ~ 60㎡이하', '60㎡초과 ~ 85㎡이하', '85㎡초과 ~ 102㎡이하', '102㎡초과 ~ 135㎡이하', '135㎡초과']
        for selectedSize in sizes:
            fileName = os.path.join(dir, 'data', 'price', '{}_{}.csv'.format(r, selectedSize))
            if os.path.isfile(fileName):
                pass
            else:
                if not os.path.isdir(os.path.join(dir, 'data', 'price')):
                    os.mkdir(os.path.join(dir, 'data', 'price'))
                csvFiles = []
                for f in fileList:
                    if '.csv' in f:
                        salesPoint = pd.read_csv(os.path.join(path, f), encoding='utf-8')
                        if not '지역' in salesPoint.columns:
                            salesPoint = salesPoint[
                                (salesPoint['지역2'] == regionDict[r]) & (salesPoint['규모'] == selectedSize)]
                            salesPoint = salesPoint.drop(['지역1', '지역2', '규모'], axis=1)
                        else:
                            salesPoint = salesPoint[salesPoint['지역'] == r]
                            salesPoint = salesPoint.drop(
                                [salesPoint.columns[0], salesPoint.columns[1], salesPoint.columns[2]], axis=1)
                        salesPoint = salesPoint.T
                        salesPoint = salesPoint.reset_index()
                        salesPoint.columns = ['날짜', f[:-4]]
                        csvFiles.append(salesPoint)
                salesPoint = pd.DataFrame.merge(csvFiles[0], csvFiles[1])
                for f in range(len(csvFiles) - 2):
                    salesPoint = pd.DataFrame.merge(salesPoint, csvFiles[f + 2])
                salesPoint.to_csv(fileName, encoding='utf-8', index=False)

def preprocessDongData(dir):
    data = {}

    data['SalesData'] = loadSalesData(dir)
    data['MainData'] = preprocessMainData(dir)
    data['DongData'] = pd.DataFrame(data['SalesData']['시군구'].value_counts()).reset_index()
    data['DongData'].columns = ['시군구', '수']
    data['DongData'] = data['DongData'][data['DongData']['수'] >= 100].reset_index(drop=True)

    for selectedDong in list(data['DongData']['시군구']):
        try:
            print(selectedDong)
            selectedDf = data['MainData'][data['MainData']['시군구'] == selectedDong].reset_index(drop=True)
            regions = list(set(list(selectedDf['시군구'])))
            newDf = []
            for r in regions:
                selectedRegion = r.split(' ')[1]
                tmp_ = selectedDf[selectedDf['시군구'] == r].reset_index(drop=True)
                sizes = list(set(list(tmp_['전용면적(㎡)'])))
                for s in sizes:
                    tmp = tmp_[tmp_['전용면적(㎡)'] == s].reset_index(drop=True)
                    if s > 40:
                        if s <= 60:
                            selectedSize = '40㎡초과 ~ 60㎡이하'
                        elif s <= 85:
                            selectedSize = '60㎡초과 ~ 85㎡이하'
                        elif s <= 102:
                            selectedSize = '85㎡초과 ~ 102㎡이하'
                        elif s <= 135:
                            selectedSize = '102㎡초과 ~ 135㎡이하'
                        else:
                            selectedSize = '135㎡초과'

                        fileName = os.path.join(dir, 'data', 'price',
                                                '{}_{}.csv'.format(selectedRegion, selectedSize))
                        salesPoint = pd.read_csv(fileName, encoding='utf-8')
                        scaler = MinMaxScaler()
                        salesPoint[salesPoint.columns[1:]] = pd.DataFrame(
                            scaler.fit_transform(salesPoint[salesPoint.columns[1:]]))

                        dropIdx = []
                        arr = []
                        for idx in range(tmp.shape[0]):
                            try:
                                changedDate = dateChange(tmp['계약일'][idx])
                                arr.append(salesPoint[salesPoint['날짜'] == changedDate]['주간아파트규모별매매가격지수'].values[0])
                            except Exception as e:
                                dropIdx.append(idx)
                                pass
                        tmp = tmp.drop(dropIdx).reset_index(drop=True)
                        tmp['주간아파트규모별매매가격지수'] = arr
                        newDf.append(tmp)


            newDf = pd.concat(newDf).reset_index(drop=True)
            newDf['선호도'] = [None] * newDf.shape[0]
            newDf.to_csv(os.path.join(dir, 'data', 'dong', '{}.csv'.format(selectedDong)), encoding='utf-8', index=False)
        except Exception as e:
            print(e.args)
            print('--------------------------------' + selectedDong)
            pass

def preprocessMainData(dir):
    data = {}
    data['SalesData'] = loadSalesData(dir)
    data['InnerData'] = loadInnerData(dir)
    data['InnerData2'] = loadInnerData2(dir)
    selectedVar = ['시군구', '번지', '단지명', '전용면적(㎡)', '계약일', '거래금액(만원)', '층', '건축년도', '학군', '역']
    data['MainData'] = pd.DataFrame.merge(data['SalesData'], data['InnerData'], on=['시군구', '번지'])[selectedVar]
    data['MainData'] = pd.DataFrame.merge(data['MainData'], data['InnerData2'][['시군구', '번지', '총층수', '동수', '시공사']],
                                          on=['시군구', '번지'])
    return data['MainData']
