import numpy as np
from typing import List, Tuple
from collections import Counter
from DataProcessing.ORM import *

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
        # 构建词袋类别-文件词袋dict
        trainClassSet = self.buildClassWord(trainSet, classSet)
        # 计算文件预测词袋
        self.tf = self.buildTfIdfWord(trainClassSet)

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

    # 构建词袋模型
    def buildClassWord(self, trainSet, classSet):
        trainClassSet = []
        for index, item in enumerate(classSet):
            wordTemp = trainSet[index]
            word = self._buildWordDict(wordTemp)
            trainClassSet.append([item, word])

        return trainClassSet

    # 计算核心
    def buildTfIdfWord(self, trainClassSet: List[List]):
        print("正在构建TF")
        return trainClassSet

    # 预测
    def Prediction(self, testSet, cnt):
        preClass = []
        for item in testSet:
            words = self._buildWordDict(item)
            preClass.append(self._PredictionOne(words, cnt))
        return preClass

    # 预测单个,不能调用
    def _PredictionOne(self, wordsTest, cnt):
        # 最小值列表(从小到大)
        preClass = [("", sys.maxsize)]
        i = 0
        for [key, words] in self.tf:
            weight = self._calculate(wordsTest, words)
            preClass = self.insertPreClass(preClass, weight, key, cnt)
        counter = Counter([key for [key, v] in preClass])

        return counter.most_common().pop(0)[0]  # 返回频率最高的类别

    def insertPreClass(self, preClass: List, weight, key, cnt):
        if weight >= preClass[-1][1]:
            return preClass

        for index in range(len(preClass)):
            item = preClass[index]
            if item[1] >= weight:
                if len(preClass) == cnt:
                    preClass[index] = [key, weight]
                else:
                    preClass.insert(index, [key, weight])
        return preClass

    # 夹角余弦
    def _calculate(self, words1, words2):
        return np.sum(words1 * words2.T) / (np.sqrt(np.sum(words1.T * words1)) * np.sqrt(np.sum(words2.T * words2)))
