import numpy as np
from typing import List, Dict
from DataProcessing.ORM import *
import sys
from collections import Counter


# 朴素贝叶斯(词集模型,离散型)
class NaiveBayes:

    def savePickle(self, path, fileName):
        ORM.writePickle(path, fileName, self)

    @staticmethod
    def loadPickle(path):
        return ORM.loadPickle(path)

    def __init__(self):
        # 词集模型,{name:矩阵},每个分类都有自己的词集
        self.setWords = {}
        # 词名key->词集模型中的index值
        self.wordIndex = {}
        # class
        # 类别概率
        self.classP = {}
        self.classList = []
        self.classIndex = {}

    # trainSet训练集(list)
    def fit(self, trainSet: List, classSet):
        # 对类型进行归类,并计算概率
        self.classList, self.classIndex, self.classP = self.categoryIndex(classSet)
        # 建立词集索引
        self.wordIndex = self.buildWordIndex(trainSet)
        # 构建词集类别-文件词集dict
        classWords = self.buildClassWord(trainSet, classSet)
        # 计算文件预测词集
        self.setWords = self.buildsetWord(classWords)

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
        lst = np.zeros((1, len(self.wordIndex)))
        for word in words:
            if word in self.wordIndex:
                lst[0, self.wordIndex[word]] = 1
        return lst[0]

    # 构建词集模型
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
    def buildsetWord(self, classWords: Dict):
        setWords = {}
        for key, item in classWords.items():
            setWordsTemp = np.zeros((1, len(self.wordIndex)))
            for words in item:
                setWordsTemp += words
            # 无拉普拉斯修正
            # setWordsTemp = setWordsTemp / (len(item))  # 除以文件数
            # setWordsTemp += 0.000000000000001  # 去0
            # 优化后的拉普拉斯修正(0.0000000000001)越小精度越高
            setWordsTemp = (setWordsTemp / len(item))
            setWords[key] = setWordsTemp
        return setWords
        # 预测

    def Prediction(self, testSet):
        preClass = []
        for item in testSet:
            words = self._buildWordDict(item)
            preClass.append(self._PredictionOne(words))
        return preClass

        # 预测单个,不能调用

    def _PredictionOne(self, words):
        minInfo = ["", -sys.maxsize]
        for key, setWords in self.setWords.items():
            weight = self.classP[key] * np.sum(
                np.log(np.abs(setWords + words - 1.0).clip(min=1/sys.maxsize)))  # P(A/B)正比于P(A)*P(B/A)
            # 不乘P(A)效果更好,乘P(A)可能是考虑样本不均匀且大样本覆盖面比较广,只有样本显著差异时才可以预测为小样本
            # weight = np.sum(np.log(np.abs(setWords + words - 1)))
            if weight > minInfo[1]:
                minInfo = (key, weight)
        return minInfo[0]
