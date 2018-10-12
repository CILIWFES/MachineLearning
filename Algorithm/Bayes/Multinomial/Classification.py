import numpy as np
from typing import List
from DataProcessing.ORM import *
from sklearn.naive_bayes import MultinomialNB


# 朴素贝叶斯(事件集模型,离散型)
class Classification:

    def savePickle(self, path, fileName):
        ORM.writePickle(path, fileName, self)

    @staticmethod
    def loadPickle(path):
        return ORM.loadPickle(path)

    def __init__(self):

        # 事件名key->事件集模型中的index值
        self.eventsIndex = {}
        self.MBN: MultinomialNB

    # trainSet训练集(list)
    def fit(self, trainSet: List, classSet):
        # 建立事件集索引
        self.eventsIndex = self._BuildEventIndex(trainSet)

        trainSet = [self._MakeEvent(item, True) for item in trainSet]
        self.MBN = MultinomialNB(alpha=0.001).fit(trainSet, classSet)

    # 建立事件集索引
    def _BuildEventIndex(self, trainSet):
        setTemp = set()
        avgFile = 0
        for item in trainSet:
            avgFile += len(item)
            itemSet = set(item)
            setTemp.update(itemSet)
        EventIndex = {name: index for index, name in enumerate(setTemp)}
        return EventIndex


    # 对单一事件生成事件集
    def _MakeEvent(self, events: List, isBag=True):
        # 新建初始长度为事件表的矩阵
        lst = np.zeros((1, len(self.eventsIndex)))
        for event in events:
            if event in self.eventsIndex:
                if isBag:
                    # 袋模型
                    lst[0, self.eventsIndex[event]] += 1
                else:
                    # 集模型
                    lst[0, self.eventsIndex[event]] = 1

        return lst[0]

    # 预测
    def Prediction(self, testSet):
        for index in range(len(testSet)):
            testSet[index] = self._MakeEvent(testSet[index])
        preClass = self.MBN.predict(testSet)
        return preClass.tolist()