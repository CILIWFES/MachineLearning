import numpy as np
from DataProcessing.Pretreatment import *
from typing import List, Dict
from DataProcessing.ORM import *
import sys


# 朴素贝叶斯
class NaiveBayes:

    def savePickle(self, path, fileName):
        ORM.writePickle(path, fileName, self)

    @staticmethod
    def loadPickle(path):
        return ORM.loadPickle(path)

    def __init__(self):
        # 词袋模型,{name:矩阵},每个分类都有自己的词袋
        self.bagWords = {}
        # 词名key->词袋模型中的index值
        self.wordIndex = {}
        # class
        self.classList = []
        self.classIndex = {}

    # trainSet训练集(list)
    def fit(self, trainSet: List, classSet):
        trainSet = [Pretreatment.filterWord(item) for item in trainSet]
        self.classList, self.classIndex = self.categoryIndex(classSet)
        self.wordIndex = self.buildWordIndex(trainSet)
        classWords = self.buildClassWord(trainSet, classSet)
        self.bagWords = self.buildBagWord(classWords)

    # 预测多个
    def Prediction(self, testSet):
        testSet = [Pretreatment.filterWord(item) for item in testSet]
        preClass = []
        for item in testSet:
            words = np.mat(self._buildWordDict(item))
            preClass.append(self._PredictionOne(words))
        return preClass

    # 预测单个,不能调用
    def _PredictionOne(self, words):
        words = words + 1 / np.sum(words)
        words = words / (np.sum(words))
        minInfo = ["", -sys.maxsize]
        for key, bagWords in self.bagWords.items():
            weight = np.sum(np.log(np.multiply(words, bagWords)))  # ln(x1*y1)的总和
            if weight > minInfo[1]:
                minInfo = (key, weight)
        return minInfo[0]

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
        classIndex = {key: index for index, key in enumerate(self.classList)}
        return classList, classIndex

    # 创建字典表
    def _buildWordDict(self, words: List):
        # 新建初始长度为词典表的矩阵
        lst = np.zeros((1, len(self.wordIndex)))
        for word in words:
            if word in self.wordIndex:
                lst[0, self.wordIndex[word]] += 1
        return lst

    # 构建词袋模型
    def buildClassWord(self, trainSet, classSet):
        classWords = {}
        for index, item in enumerate(classSet):
            wordTemp = trainSet[index]
            word = self._buildWordDict(wordTemp)
            if item in classWords:
                classWords[item].append(word)
            else:
                classWords[item] = [word]
        return classWords

    # 计算核心
    def buildBagWord(self, classWords: Dict):
        print("正在构建词袋")
        bagWords = {}
        for key, item in classWords.items():
            print("构建词袋:", key)
            bagWordsTemp = np.zeros((1, len(self.wordIndex)))
            for words in item:
                bagWordsTemp += words  # (词袋频率+1/分类数)/相对平均文本长度比例
            bagWordsTemp = bagWordsTemp + 1 / np.sum(bagWordsTemp)
            bagWordsTemp = bagWordsTemp / float(np.sum(bagWordsTemp))  # 除以文件数
            bagWords[key] = bagWordsTemp
        return bagWords
