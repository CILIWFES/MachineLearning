import numpy as np
from typing import List
from collections import Counter
from DataProcessing.ORM import *
import math
import sys


# 默认KNN
class KNNClassifier:
    def SavePickle(self, path, fileName):
        ORM.writePickle(path, fileName, self)

    @staticmethod
    def LoadPickle(path):
        return ORM.LoadPickle(path)

    def __init__(self):
        # 特征频率
        self.frequency = {}
        # 计算核心
        self.calculateModel = None
        # 特征名索引
        self.featureIndex = {}
        # 类别概率
        self.classList = []
        self.classIndex = {}

    # trainSet训练集(list)
    def fit(self, trainSet: List, classSet):
        # 对类型进行归类,并计算概率
        self.classList, self.classIndex = self._BuildCategoryIndex(classSet)
        # 建立特征袋索引
        self.featureIndex = self._BuildFeatureIndex(trainSet)
        # 构建计算核心
        self.calculateModel = self._BuildCalculateModel(trainSet, classSet)

    # 构建特征袋name->index坐标索引
    def _BuildFeatureIndex(self, trainSet):
        setTemp = set()
        avgFile = 0
        for item in trainSet:
            avgFile += len(item)
            itemSet = set(item)
            setTemp.update(itemSet)
        featureIndex = {name: index for index, name in enumerate(setTemp)}
        return featureIndex

    # 建立类别索引
    def _BuildCategoryIndex(self, classSet):
        classList = list(set(classSet))
        classIndex = {key: index for index, key in enumerate(classList)}
        # P(A)概率,拉普拉斯修正
        return classList, classIndex

    # 创建字典表
    def _BuildFeatureDict(self, features: List):
        # 新建初始长度为特征典表的矩阵
        lst = np.zeros((1, len(self.featureIndex)))
        for feature in features:
            if feature in self.featureIndex:
                lst[0, self.featureIndex[feature]] += 1
        return lst[0]

    # 构建计算核心
    def _BuildCalculateModel(self, trainSet, classSet):
        trainClassSet = []
        for index, item in enumerate(classSet):
            featureTemp = trainSet[index]
            feature = self._BuildFeatureDict(featureTemp)
            feature = feature / np.sum(feature)
            # key值,特征频,向量的模
            trainClassSet.append([item, feature, math.sqrt(np.sum(np.power(feature, 2)))])
        return trainClassSet

    # 预测
    def Prediction(self, testSet, cnt):
        preClass = []
        for item in testSet:
            features = self._BuildFeatureDict(item)
            features = features / np.sum(features)
            sizeTest = math.sqrt(np.sum(np.power(features, 2)))
            preClass.append(self._PredictionOne(features, sizeTest, cnt))
        return preClass

    # 预测单个,不能调用
    def _PredictionOne(self, featuresTest, sizeTest, cnt):
        # 最小值列表(从小到大)
        preClass = [("", -sys.maxsize)]
        for [key, featuresTrain, sizeTrain] in self.calculateModel:
            weight = self._calculate(featuresTest, sizeTest, featuresTrain, sizeTrain)
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

    def _calculate(self, featuresTest, sizeTest, featuresTrain, sizeTrain):
        inner = np.sum(np.multiply(featuresTest, featuresTrain))
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
    def _BuildCalculateModel(self, trainSet, classSet):
        trainClassSet = []
        for index, item in enumerate(classSet):
            featureTemp = trainSet[index]
            feature = self._BuildFeatureDict(featureTemp)
            feature = feature / np.sum(feature)
            # key值,特征频,向量的模
            trainClassSet.append([item, self._OptimizationFeatures(feature), math.sqrt(np.sum(np.power(feature, 2)))])
        return trainClassSet

    # 夹角余弦
    def _calculate(self, featuresTest, sizeTest, calcuteTrain, sizeTrain):
        sum = 0
        for (index, cnt) in calcuteTrain:
            sum += featuresTest[index] * cnt
        return sum / (sizeTest * sizeTrain)

    def _OptimizationFeatures(self, features):
        lst = [(index, cnt) for index, cnt in enumerate(features) if cnt > 0]
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
            features = self._BuildFeatureDict(item)
            features = features / np.sum(features)
            sizeTest = math.sqrt(np.sum(np.power(features, 2)))
            calculateFeatures = self._OptimizationFeatures(features)
            preClass.append(self._PredictionOne(calculateFeatures, sizeTest, cnt))
        return preClass

    # 夹角余弦
    def _calculate(self, calcuteTest, sizeTest, featuresTrain, sizeTrain):
        sum = 0
        for (index, cnt) in calcuteTest:
            sum += featuresTrain[index] * cnt
        return sum / (sizeTest * sizeTrain)

    def _OptimizationFeatures(self, features):
        lst = [(index, cnt) for index, cnt in enumerate(features) if cnt > 0]
        return lst


"""
*****************************************************************************************************
"""


# 以类别来分类(没有效果)
class KNNClassifier_Class(KNNClassifier):

    # 构建计算核心
    def buildCalculateFeature(self, trainSet, classSet):
        trainClassSet = []
        classCalculateFeature = {}
        # 归类
        for index, item in enumerate(classSet):
            featureTemp = trainSet[index]
            feature = self._BuildFeatureDict(featureTemp)
            feature = feature / np.sum(feature)
            if classSet[index] in trainClassSet:
                classCalculateFeature[classSet[index]].append(feature)
            else:
                classCalculateFeature[classSet[index]] = [feature]
        # 以类来评估
        for key, item in classCalculateFeature.items():
            itemMatrix = np.mat(item)
            itemMatrix = itemMatrix / np.sum(itemMatrix)
            # key值,特征频,向量的模
            trainClassSet.append([key, itemMatrix[0], math.sqrt(np.sum(np.power(itemMatrix, 2)))])
        return trainClassSet
