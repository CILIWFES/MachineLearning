from sklearn.naive_bayes import MultinomialNB
from typing import List
from DataProcessing.Pretreatment import *
from DataProcessing.ORM import *
import numpy as np
from collections import Counter


# 多项式(离散型)贝叶斯
class Multinomial_NB:
    def savePickle(self, path, fileName):
        ORM.writePickle(path, fileName, self)

    @staticmethod
    def loadPickle(path):
        return ORM.loadPickle(path)

    def __init__(self):
        self.MBN = None
        self.classList = None
        self.wordIndex = None
        self.classIndex = None
        self.classP = None

    def fit(self, trainSet: List, classSet):
        # 建立词典索引
        self.wordIndex = self.buildWordIndex(trainSet)
        # 构建 词袋/词集
        trainSet = [self._buildWordDict(item) for item in trainSet]
        # alpha:0.001,alpha越小,遍历次数越高
        self.MBN = MultinomialNB(alpha=0.001).fit(trainSet, classSet)

    # 建立类别索引
    def categoryIndex(self, classSet):
        classList = list(set(classSet))
        classIndex = {key: index for index, key in enumerate(classList)}
        # P(A)概率,拉普拉斯修正
        classP = {key: (v + 1) / (len(classSet) + len(classIndex)) for key, v in dict(Counter(classSet)).items()}
        return classList, classIndex, classP

    # 创建字典表
    def _buildWordDict(self, words: List):
        # 新建初始长度为词典表的矩阵
        # lst = [0 for i in range(len(self.wordIndex))]
        lst = np.zeros((1, len(self.wordIndex)))
        for word in words:
            if word in self.wordIndex:
                # # 词集
                # lst[0, self.wordIndex[word]] = 1
                # 词袋(准确度更高)
                lst[0, self.wordIndex[word]] += 1
        return lst[0]

    # 构建词集name->index坐标索引
    def buildWordIndex(self, trainSet):
        setTemp = set()
        avgFile = 0
        for item in trainSet:
            avgFile += len(item)
            itemSet = set(item)
            setTemp.update(itemSet)
        wordIndex = {name: index for index, name in enumerate(setTemp)}
        return wordIndex

    def Prediction(self, testSet: List):
        for index in range(len(testSet)):
            testSet[index] = self._buildWordDict(testSet[index])
        preClass = self.MBN.predict(testSet)
        return preClass.tolist()
