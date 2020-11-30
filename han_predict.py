import os

import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, CSVLogger
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import SimpleRNN
from tensorflow.keras.regularizers import L1L2
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from han_loadData import loadPricePointData
from han_utils import makeDataset

def predictPricePoint(dir, gu, size, showgraph, test_rate, window_size, after, is_train):
    df = loadPricePointData(dir, gu, size)
    TEST_SIZE = int(df.shape[0] * test_rate)
    train = df[:-TEST_SIZE]
    test = df[-TEST_SIZE:]
    # 이용할 변수들의 이름 선언
    #featureCols = ['주간아파트매매가격지수', '주간아파트규모별매매가격지수', '주간아파트규모별전세가격지수', '주간아파트전세가격지수']
    featureCols = ['주간아파트규모별매매가격지수']
    labelCol = ['주간아파트규모별매매가격지수']
    # 독립변수와 종속변수 분리
    trainFeature = train[featureCols]
    trainLabel = train[labelCol]
    X_test = test[featureCols]
    y_test = test[labelCol]
    # train dataset 생성
    trainFeature, trainLabel = makeDataset(trainFeature, trainLabel, window_size, after)
    # train, validation set 생성
    X_train, X_valid, y_train, y_valid = train_test_split(trainFeature, trainLabel, test_size=0.1)
    # test dataset (실제 예측 해볼 데이터) 생성
    X_test, y_test = makeDataset(X_test, y_test, window_size, after)
    # 최종 결과값, 즉 두달 뒤의 아파트 매매가격 지수
    realPredFeature = np.reshape(np.array(df[-window_size:][featureCols]), (1, window_size, 1))

    print(X_train.shape)
    print(X_test.shape)
    model = Sequential()
    model.add(LSTM(5,
                   input_shape=(trainFeature.shape[1], trainFeature.shape[2]),
                   activation='relu',
                   return_sequences=True
                   )
              )
    model.add(LSTM(15,
                   activation='relu',
                   return_sequences=True
                   )
              )
    model.add(LSTM(25,
                   activation='relu',
                   return_sequences=False
                   )
              )
    model.add(Dense(1))
    model.summary()

    callback_filename = os.path.join('test.h5')

    callback_list = []
    model.compile(optimizer=Adam(), loss='mse')
    callback_list.append(EarlyStopping(monitor='val_loss', patience=5))
    callback_list.append(ModelCheckpoint(callback_filename, monitor='val_loss', verbose=1, save_best_only=True, mode='auto'))

    if is_train:
        model.fit(X_train, y_train,
                    epochs=100,
                    batch_size=1,
                    validation_data=(X_valid, y_valid),
                    callbacks=callback_list)

    model.load_weights(callback_filename)

    # 예측
    pred = model.predict(X_test)
    pred = np.array(pred)

    if showgraph:
        # 실제 종가와 예측한 종가를  그래프로 비교
        plt.figure(figsize=(12, 9))
        plt.plot(train['날짜'], train['주간아파트규모별매매가격지수'], color='b', label='actual')
        plt.plot(test['날짜'], test['주간아파트규모별매매가격지수'], color='b')
        plt.plot(test['날짜'][-pred.shape[0]:], pred, label='predict', color='r')
        #plt.plot(pred, label='prediction')
        plt.legend()
        plt.savefig(os.path.join(dir, 'test.png'))

    realPredLabel = model.predict(realPredFeature)
    return realPredLabel