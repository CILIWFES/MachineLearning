import numpy as np
from typing import List, Tuple
from collections import Counter
from DataProcessing.ORM import *
import math
import sys


class KNNClassifier:
    def savePickle(self, path, fileName):
        ORM.writePickle(path, fileName, self)

    @staticmethod
    def loadPickle(path):
        return ORM.loadPickle(path)

    def __init__(self):
        # 词袋模型,{name:矩阵},每个分类都有自己的词袋
        self.tf = {}
        # 词名key->词袋模型中的index值
        self.wordIndex = {}
        # 类别概率
        self.classList = []
        self.classIndex = {}

    # trainSet训练集(list)
    def fit(self, trainSet: List, classSet):
        # 对类型进行归类,并计算概率
        self.classList, self.classIndex = self.categoryIndex(classSet)
        # 建立词袋索引
        self.wordIndex = self.buildWordIndex(trainSet)
        # 构建计算核心
        self.calculate = self.buildCalculateWord(trainSet, classSet)

    # 构建词袋name->index坐标索引
    def buildWordIndex(self, trainSet):
        setTemp = set()
        avgFile = 0
        for item in trainSet:
            avgFile += len(item)
            itemSet = set(item)
            setTemp.update(itemSet)
        wordIndex = {name: index for index, name in enumerate(setTemp)}
        return wordIndex

    # 建立类别索引
    def categoryIndex(self, classSet):
        classList = list(set(classSet))
        classIndex = {key: index for index, key in enumerate(classList)}
        # P(A)概率,拉普拉斯修正
        return classList, classIndex

    # 创建字典表
    def _buildWordDict(self, words: List):
        # 新建初始长度为词典表的矩阵
        lst = np.zeros((1, len(self.wordIndex)))
        for word in words:
            if word in self.wordIndex:
                lst[0, self.wordIndex[word]] += 1
        return lst[0]

    # 构建计算核心
    def buildCalculateWord(self, trainSet, classSet):
        trainClassSet = []
        for index, item in enumerate(classSet):
            wordTemp = trainSet[index]
            word = self._buildWordDict(wordTemp)
            word = word / np.sum(word)
            # key值,词频,向量的模
            trainClassSet.append([item, word, math.sqrt(np.sum(np.power(word, 2)))])
        return trainClassSet

    # 预测
    def Prediction(self, testSet, cnt):
        preClass = []
        for item in testSet:
            words = self._buildWordDict(item)
            words = words / np.sum(words)
            preClass.append(self._PredictionOne(words, cnt))
        return preClass

    # 预测单个,不能调用
    def _PredictionOne(self, wordsTest, cnt):
        # 最小值列表(从小到大)
        preClass = [("", -sys.maxsize)]
        size = math.sqrt(np.sum(np.power(wordsTest, 2)))
        for [key, words, size2] in self.calculate:
            weight = self._calculate(wordsTest, size, words, size2)
            preClass = self.insertPreClass(preClass, weight, key, cnt)
        counter = Counter([key for (key, v) in preClass])

        return counter.most_common().pop(0)[0]  # 返回频率最高的类别

    def insertPreClass(self, preClass: List, weight, key, cnt):
        if weight <= preClass[-1][1]:
            return preClass

        for index in range(len(preClass)):
            item = preClass[index]
            if item[1] <= weight:
                if len(preClass) == cnt:
                    preClass[index] = [key, weight]
                else:
                    preClass.insert(index, (key, weight))
        return preClass

    # 夹角余弦
    def _calculate(self, words1, size1, words2, size2):
        return np.sum(np.multiply(words1, words2)) / (size1 * size2)
