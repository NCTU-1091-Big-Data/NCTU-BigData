# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 19:02:15 2020

@author: ASUS
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix


df = pd.read_csv('all_feature_data.csv')
colume = df.keys()

x = df.drop(['title','type'],axis=1)
y = df['type']


from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
labelencoder = LabelEncoder()
y_label = labelencoder.fit_transform(y)



X_train, X_test, y_train, y_test = train_test_split(x, y_label, 
                                                    test_size= 0.2,
                                                    random_state= 1)


reg = LinearRegression().fit(X_train, y_train)

pretest = reg.predict(X_test)


'''
multinomial LogisticRegression 
'''
from sklearn.linear_model import LogisticRegression



X_train, X_test, y_train, y_test = train_test_split(x, y, 
                                                    test_size= 0.2,
                                                    random_state= 1)

reg = LogisticRegression().fit(X_train, y_train)

pretest = reg.predict(X_test)

confusion_matrix(y_test, pretest,
                 labels=["FA", "GA", "B", "C", "Start","Stub"])

from sklearn import metrics
# 計算精度
print("Accuracy : %.4g" % metrics.accuracy_score(y_test, pretest))


'''
DecisionTreeClassifier
''' 
from sklearn.tree import DecisionTreeClassifier

X_train, X_test, y_train, y_test = train_test_split(x, y, 
                                                    test_size= 0.2,
                                                    random_state= 1)

reg = DecisionTreeClassifier().fit(X_train, y_train)

pretest = reg.predict(X_test)

confusion_matrix(y_test, pretest,
                 labels=["FA", "GA", "B", "C", "Start","Stub"])

from sklearn import metrics
# 計算精度
print("Accuracy : %.4g" % metrics.accuracy_score(y_test, pretest))


'''
RandomForestClassifier
'''
from sklearn.ensemble import RandomForestClassifier
X_train, X_test, y_train, y_test = train_test_split(x, y, 
                                                    test_size= 0.2,
                                                    random_state= 1)

clf = RandomForestClassifier(max_depth=4, random_state=1).fit(X_train, y_train)
pretest = clf.predict(X_test)

confusion_matrix(y_test, pretest,
                 labels=["FA", "GA", "B", "C", "Start","Stub"])

from sklearn import metrics
# 計算精度
print("Accuracy : %.4g" % metrics.accuracy_score(y_test, pretest))


'''
xgboost
'''
from xgboost.sklearn import XGBClassifier
clf = XGBClassifier(
        #樹的個數
        n_estimators=100,
        # 如同學習率
        learning_rate= 0.3, 
        # 構建樹的深度，越大越容易過擬合    
        max_depth=6, 
        # 隨機取樣訓練樣本 訓練例項的子取樣比
        subsample=1, 
        # 用於控制是否後剪枝的引數,越大越保守，一般0.1、0.2這樣子
        gamma=0, 
        # 控制模型複雜度的權重值的L2正則化項引數，引數越大，模型越不容易過擬合。
        reg_lambda=1,  
        
        #最大增量步長，我們允許每個樹的權重估計。
        max_delta_step=0,
        # 生成樹時進行的列取樣 
        colsample_bytree=1, 

        # 這個引數預設是 1，是每個葉子裡面 h 的和至少是多少，對正負樣本不均衡時的 0-1 分類而言
        # 假設 h 在 0.01 附近，min_child_weight 為 1 意味著葉子節點中最少需要包含 100 個樣本。
        #這個引數非常影響結果，控制葉子節點中二階導的和的最小值，該引數值越小，越容易 overfitting。
        min_child_weight=1, 

        #隨機種子
        seed=1000 
        
        # L1 正則項引數
#        reg_alpha=0,
        
        #如果取值大於0的話，在類別樣本不平衡的情況下有助於快速收斂。平衡正負權重
        #scale_pos_weight=1,
        
        #多分類的問題 指定學習任務和相應的學習目標
        #objective= 'multi:softmax', 
        
        # 類別數，多分類與 multisoftmax 並用
        #num_class=10,
        
        # 設定成1則沒有執行資訊輸出，最好是設定為0.是否在執行升級時列印訊息。
#        silent=0 ,
        # cpu 執行緒數 預設最大
#        nthread=4,
    
        #eval_metric= 'auc'
)
# 模型 訓練
clf.fit(X_train,y_train,eval_metric='auc')
# 預測值
y_pred=clf.predict(X_test)
# 真實值 賦值
y_true= y_test

confusion_matrix(y_test, y_pred,
                 labels=["FA", "GA", "B", "C", "Start","Stub"])


from sklearn import metrics
# 計算精度
print("Accuracy : %.4g" % metrics.accuracy_score(y_true, y_pred))


from sklearn import svm

clf = svm.SVC(decision_function_shape='ovr')
clf.fit(X_train,y_train)
y_pred=clf.predict(X_test)


confusion_matrix(y_test, y_pred,
                 labels=["FA", "GA", "B", "C", "Start","Stub"])

from sklearn import metrics
# 計算精度
print("Accuracy : %.4g" % metrics.accuracy_score(y_test, pretest))