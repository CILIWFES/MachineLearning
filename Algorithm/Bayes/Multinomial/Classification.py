import numpy as np
from typing import List
from DataProcessing.ORM import *
from sklearn.naive_bayes import MultinomialNB


# 朴素贝叶斯(特征集模型,离散型)
class Classification:

    def SavePickle(self, path, fileName):
        ORM.writePickle(path, fileName, self)

    @staticmethod
    def LoadPickle(path):
        return ORM.LoadPickle(path)

    def __init__(self):

        # 特征名key->特征集模型中的index值
        self.FeaturesIndex = {}
        self.MBN: MultinomialNB

    # trainSet训练集(list)
    def fit(self, trainSet: List, classSet):
        # 建立特征集索引
        self.FeaturesIndex = self._BuildFeatureIndex(trainSet)

        trainSet = [self._MakeFeature(item, True) for item in trainSet]
        self.MBN = MultinomialNB(alpha=0.001).fit(trainSet, classSet)

    # 建立特征集索引
    def _BuildFeatureIndex(self, trainSet):
        setTemp = set()
        avgFile = 0
        for item in trainSet:
            avgFile += len(item)
            itemSet = set(item)
            setTemp.update(itemSet)
        FeatureIndex = {name: index for index, name in enumerate(setTemp)}
        return FeatureIndex


    # 对单一特征生成特征集
    def _MakeFeature(self, Features: List, isBag=True):
        # 新建初始长度为特征表的矩阵
        lst = np.zeros((1, len(self.FeaturesIndex)))
        for Feature in Features:
            if Feature in self.FeaturesIndex:
                if isBag:
                    # 袋模型
                    lst[0, self.FeaturesIndex[Feature]] += 1
                else:
                    # 集模型
                    lst[0, self.FeaturesIndex[Feature]] = 1

        return lst[0]

    # 预测
    def Prediction(self, testSet):
        for index in range(len(testSet)):
            testSet[index] = self._MakeFeature(testSet[index])
        preClass = self.MBN.predict(testSet)
        return preClass.tolist()