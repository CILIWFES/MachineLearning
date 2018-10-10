import numpy as np
from typing import List, Tuple
from collections import Counter
from DataProcessing.ORM import *
import math
import sys


# 默认KNN
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
            sizeTest = math.sqrt(np.sum(np.power(words, 2)))
            preClass.append(self._PredictionOne(words, sizeTest, cnt))
        return preClass

    # 预测单个,不能调用
    def _PredictionOne(self, wordsTest, sizeTest, cnt):
        # 最小值列表(从小到大)
        preClass = [("", -sys.maxsize)]
        for [key, wordsTrain, sizeTrain] in self.calculate:
            weight = self._calculate(wordsTest, sizeTest, wordsTrain, sizeTrain)
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

    def _calculate(self, wordsTest, sizeTest, wordsTrain, sizeTrain):
        inner = np.sum(np.multiply(wordsTest, wordsTrain))
        return self._Cos(inner, sizeTest, sizeTrain)

    # 夹角余弦
    def _Cos(self, inner, module1, module2):
        return inner / (module1 * module2)

    # 闵科夫斯基距离
    def _MinkowskiDistance(self, plot1, plot2, powerNumber: int):
        sum = np.abs(np.power(plot1 - plot2, powerNumber)).sum()
        distance = math.pow(sum, 1.0 / powerNumber)
        return distance

    # 欧式距离(没效果)
    def _EuclideanDistance(self, plot1, plot2):
        return self._MinkowskiDistance(plot1, plot2, 2)

    # 曼哈顿距离(没效果)
    def _ManhattonDistance(self, plot1, plot2):
        return self._MinkowskiDistance(plot1, plot2, 1)


"""
*****************************************************************************************************
"""


# 优化训练集合,大大提高空间效率,预测效率与KNN_TrainTime一致(训练效率远低于KNN_TrainTime)
class KNN_RAM(KNNClassifier):

    # 构建计算核心
    def buildCalculateWord(self, trainSet, classSet):
        trainClassSet = []
        for index, item in enumerate(classSet):
            wordTemp = trainSet[index]
            word = self._buildWordDict(wordTemp)
            word = word / np.sum(word)
            # key值,词频,向量的模
            trainClassSet.append([item, self._OptimizationWords(word), math.sqrt(np.sum(np.power(word, 2)))])
        return trainClassSet

    # 夹角余弦
    def _calculate(self, wordsTest, sizeTest, calcuteTrain, sizeTrain):
        sum = 0
        for (index, cnt) in calcuteTrain:
            sum += wordsTest[index] * cnt
        return sum / (sizeTest * sizeTrain)

    def _OptimizationWords(self, words):
        lst = [(index, cnt) for index, cnt in enumerate(words) if cnt > 0]
        return lst


"""
*****************************************************************************************************
"""


# 优化测试集合,预测效率与KNN_RAM一样,训练效率远高于KNN_RAM(线上懒惰模式,动态训练场景适用,若是静态训练不如KNN_RAM)
class KNN_TrainTime(KNNClassifier):

    # 预测
    def Prediction(self, testSet, cnt):
        preClass = []
        for item in testSet:
            words = self._buildWordDict(item)
            words = words / np.sum(words)
            sizeTest = math.sqrt(np.sum(np.power(words, 2)))
            calculateWords = self._OptimizationWords(words)
            preClass.append(self._PredictionOne(calculateWords, sizeTest, cnt))
        return preClass

    # 夹角余弦
    def _calculate(self, calcuteTest, sizeTest, wordsTrain, sizeTrain):
        sum = 0
        for (index, cnt) in calcuteTest:
            sum += wordsTrain[index] * cnt
        return sum / (sizeTest * sizeTrain)

    def _OptimizationWords(self, words):
        lst = [(index, cnt) for index, cnt in enumerate(words) if cnt > 0]
        return lst


"""
*****************************************************************************************************
"""


# 以类别来分类(没有效果)
class KNNClassifier_Class(KNNClassifier):

    # 构建计算核心
    def buildCalculateWord(self, trainSet, classSet):
        trainClassSet = []
        classCalculateWord = {}
        # 归类
        for index, item in enumerate(classSet):
            wordTemp = trainSet[index]
            word = self._buildWordDict(wordTemp)
            word = word / np.sum(word)
            if classSet[index] in trainClassSet:
                classCalculateWord[classSet[index]].append(word)
            else:
                classCalculateWord[classSet[index]] = [word]
        # 以类来评估
        for key, item in classCalculateWord.items():
            itemMatrix = np.mat(item)
            itemMatrix = itemMatrix / np.sum(itemMatrix)
            # key值,词频,向量的模
            trainClassSet.append([key, itemMatrix[0], math.sqrt(np.sum(np.power(itemMatrix, 2)))])
        return trainClassSet
