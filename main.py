import pandas as pd
from han_loadData import loadSalesData, loadInnerData, loadInnerData2, loadDongData, loadPricePointData, loadCafeData, preprocessPricePointData, preprocessDongData
from han_loadData import preprocessMainData
from han_predict import predictPricePoint

# path
dir = 'D:/han_project01/project'
# dictionary 4 all data
data = {}
preprocessDongData(dir)
# data['SalesData'] = loadSalesData(dir)
# data['InnerData'] = loadInnerData(dir)
# data['InnerData2'] = loadInnerData2(dir)
# selectedVar = ['시군구', '번지', '주소', '단지명', '전용면적(㎡)', '계약일', '거래금액(만원)', '층', '건축년도', '학군', '역']
# data['MainData'] = pd.DataFrame.merge(data['SalesData'], data['InnerData'], on=['시군구', '번지'])[selectedVar]
# data['MainData'] = pd.DataFrame.merge(data['MainData'], data['InnerData2'][['시군구', '번지', '총층수', '동수', '시공사']], on=['시군구', '번지'])

# data['DongData'] = pd.DataFrame(data['MainData']['시군구'].value_counts()).reset_index()
# data['DongData'].columns = ['시군구', '수']
# data['DongData'] = data['DongData'][data['DongData']['수'] >= 100].reset_index(drop=True)
#
# dong = '서울특별시 강남구 개포동'
# data[dong] = loadDongData(dir, dong)
# gu ='강남구'
# size = '102㎡초과 ~ 135㎡이하'
# data['{}_{}'.format(gu, size)] = loadPricePointData(dir, gu, size)
# data['cafe_{}'.format(gu)] = loadCafeData(dir, gu)

# print('\nSalesData')
# print(data['SalesData'].columns)
# print(data['SalesData'].head())
# print(data['SalesData'].shape)
# print('\nInnerData')
# print(data['InnerData'].columns)
# print(data['InnerData'].head())
# print(data['InnerData'].shape)
# print('\nInnerData2')
# print(data['InnerData2'].columns)
# print(data['InnerData2'].head())
# print(data['InnerData2'].shape)
# print('\nMainData')
# print(data['MainData'].columns)
# print(data['MainData'].head())
# print(data['MainData'].shape)
# print('\n'+dong)
# print(data[dong].columns)
# print(data[dong].head())
# print(data[dong].shape)
# print('\n{}_{}'.format(gu, size))
# print(data['{}_{}'.format(gu, size)].columns)
# print(data['{}_{}'.format(gu, size)].head())
# print(data['{}_{}'.format(gu, size)].shape)
# print('\ncafe_{}'.format(gu))
# print(data['cafe_{}'.format(gu)].columns)
# print(data['cafe_{}'.format(gu)].head())
# print(data['cafe_{}'.format(gu)].shape)
# gu ='강남구'
# size = '102㎡초과 ~ 135㎡이하'
# print(predictPricePoint(dir, gu, size, True, 0.2, 50, 13, True))
# data['MainData'] = preprocessMainData(dir)
# print('\nMainData')
# print(data['MainData'].columns)
# print(data['MainData'].head())
# print(data['MainData'].shape)
