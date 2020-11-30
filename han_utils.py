import numpy as np
import datetime

def makeDataset(data, label, window_size=20, after=4):
    feature_list = []
    label_list = []
    for i in range(len(data) - window_size -1 - after):
        feature_list.append(np.array(data.iloc[i:i+window_size]))
        label_list.append(np.array(label.iloc[i+window_size+after]))
    return np.array(feature_list), np.array(label_list)

def dateChange(d):
    d = datetime.datetime.strptime(str(d), '%Y%m%d')
    d = (d - datetime.timedelta(days=d.weekday()))
    return str(d.strftime("%Y년 %m월%d일".encode('unicode-escape').decode()).encode().decode('unicode-escape'))