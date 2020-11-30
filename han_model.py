import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
import matplotlib.font_manager as fm

mpl.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'NanumGothic'
path = 'C:/Windows/Fonts/NanumGothicBold.ttf'
font_name = fm.FontProperties(fname=path, size=50).get_name()
plt.rc('font', family=font_name)

import lightgbm as lgbm
import sklearn
from sklearn.metrics import log_loss
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score

from han_loadData import loadPreDongData
from sklearn.preprocessing import MinMaxScaler

import xgboost
from sklearn.model_selection import cross_val_score, KFold
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import explained_variance_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import r2_score,mean_absolute_error, mean_squared_error
import lightgbm as lgb
from catboost import CatBoostRegressor
import os
from sklearn.model_selection import train_test_split

# Defining two rmse_cv functions
def rmse_cv(model):
    rmse = np.sqrt(-cross_val_score(model, X_train, y_train, scoring="neg_mean_squared_error", cv = 5))
    return(np.mean(rmse))

def modelXgboot():
    xgb_model = xgboost.XGBRegressor(n_estimators=100, learning_rate=0.08, gamma=0, subsample=0.75,
                               colsample_bytree=1, max_depth=7)

    xgb_model.fit(X_train, y_train)
    predictions = xgb_model.predict(X_test)
    r_sq = xgb_model.score(X_train, y_train)
    acc = xgb_model.score(X_test, y_test)
    return rmse_cv(xgb_model), acc

def modelLinear():
    ridge_alpha = 1
    lasso_alpha = 0.1

    linear = LinearRegression()
    ridge = Ridge(alpha = ridge_alpha)
    lasso = Lasso(alpha = lasso_alpha)

    linear.fit(X_train,y_train)

    ridge.fit(X_train,y_train)

    lasso.fit(X_train,y_train)

    # MSE/MAE 비교
    linear_y_hat = linear.predict(X_test)
    ridge_y_hat = ridge.predict(X_test)
    lasso_y_hat = lasso.predict(X_test)

    linear_r2, ridge_r2, lasso_r2 = r2_score(y_test,linear_y_hat), r2_score(y_test,ridge_y_hat), r2_score(y_test,lasso_y_hat)
    linear_MSE, ridge_MSE, lasso_MSE = mean_squared_error(y_test,linear_y_hat)** 0.5, mean_squared_error(y_test,ridge_y_hat)** 0.5, mean_squared_error(y_test,lasso_y_hat)** 0.5

    return [linear_MSE, ridge_MSE]

def modelLGB():
    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

    # specify your configurations as a dict
    params = {
        'boosting_type': 'gbdt',
        'objective': 'regression',
        'metric': {'l2', 'l1'},
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': 0
    }

    # train
    gbm = lgb.train(params,
                    lgb_train,
                    num_boost_round=20,
                    valid_sets=lgb_eval,
                    early_stopping_rounds=5)

    # predict
    y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
    # eval
    return mean_squared_error(y_test, y_pred) ** 0.5

def modelCat():
    model=CatBoostRegressor(iterations=100, depth=3, learning_rate=0.1, loss_function='RMSE')
    model.fit(X_train, y_train,eval_set=(X_test, y_test),plot=True)
    return model.best_score_['validation']['RMSE']


dir = 'D:/han_project01/project'
resDf = []

dongArr = os.listdir(os.path.join(dir, 'data', 'preprocessedDong'))

for d in dongArr:
    dong = dong = d[:-4]
    tmp = loadPreDongData(dir, dong)
    selectedVar = ['전용면적(㎡)', '거래금액(만원)', '층', '건축년도', '학군', '총층수', '동수', '선호도']
    data = tmp[selectedVar]

    scaler = MinMaxScaler()
    data = pd.DataFrame(scaler.fit_transform(data))
    data.columns = selectedVar
    data[['주간아파트규모별매매가격지수', '근접역세권', '간접역세권', '비역세권', '브랜드인지도']] = tmp[
        ['주간아파트규모별매매가격지수', '근접역세권', '간접역세권', '비역세권', '브랜드인지도']]

    X = data.drop(['거래금액(만원)'], axis=1)
    y = data['거래금액(만원)']

    # 7:3으로 분리

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    print(X_train.shape)
    print(X_test.shape)

    lr = modelLinear()
    xg = modelXgboot()
    resDf.append([dong, lr[0], lr[1], xg[0], xg[1], modelLGB(), modelCat()])
resDf = pd.DataFrame(resDf)
resDf.columns = ['Region', 'Linear', 'Lasso', 'XGBoost', 'XGBoost_acc', 'Lightgbm', 'CatBoost']

arr = ['Average']
for c in resDf.columns[1:]:
    arr.append(resDf[c].mean())
newDf = pd.DataFrame(arr).T
newDf.columns = resDf.columns
newDf.to_excel(os.path.join(dir, 'resultAver.xlsx'), index=False)
resDf.to_excel(os.path.join(dir, 'resultAll.xlsx'), index=False)
print(resDf)
