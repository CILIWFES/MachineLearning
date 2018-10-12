import numpy as np
from typing import List, Dict
from DataProcessing.ORM import *
import sys
from collections import Counter


# 朴素贝叶斯(特征集模型,离散型)
class Classification:

    def SavePickle(self, path, fileName):
        ORM.writePickle(path, fileName, self)

    @staticmethod
    def LoadPickle(path):
        return ORM.LoadPickle(path)

    def __init__(self):
        # 类别特征集模型,{name:矩阵},每个分类都有自己的特征集
        self.calculateModel = {}
        # 特征名key->特征集模型中的index值
        self.featuresIndex = {}
        # class
        # 类别概率
        self.classP = {}
        self.classList = []
        self.classIndex = {}

    # trainSet训练集(list)
    def fit(self, trainSet: List, trainClass):
        # 对类型进行归类,并计算概率
        self.classList, self.classIndex, self.classP = self._BuildCategoryIndex(trainClass)
        # 建立特征集索引
        self.featuresIndex = self._BuildFeatureIndex(trainSet)
        # 构建特征集类别-文件特征集dict
        classFeatures = self._BuildClassFeature(trainSet, trainClass)
        # 计算文件预测特征集
        self.calculateModel = self._BuildCalCulteFeature(classFeatures)

    # 建立类别索引
    def _BuildCategoryIndex(self, trainClass):
        classList = list(set(trainClass))
        classIndex = {key: index for index, key in enumerate(classList)}
        # P(A)概率,拉普拉斯修正
        classP = {key: (v + 1) / (len(trainClass) + len(classIndex)) for key, v in dict(Counter(trainClass)).items()}
        return classList, classIndex, classP

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

    # 构建类别-特征集模型
    def _BuildClassFeature(self, trainSet, trainClass):
        classFeatures = {}
        for index, item in enumerate(trainClass):
            FeatureTemp = trainSet[index]
            Feature = self._MakeFeature(FeatureTemp)
            if item in classFeatures:
                classFeatures[item].append(Feature)
            else:
                classFeatures[item] = [Feature]
        return classFeatures

    # 对单一特征生成特征集
    def _MakeFeature(self, features: List):
        # 新建初始长度为特征表的矩阵
        lst = np.zeros((1, len(self.featuresIndex)))
        for feature in features:
            if feature in self.featuresIndex:
                lst[0, self.featuresIndex[feature]] = 1
        return lst[0]

    # 计算核心
    def _BuildCalCulteFeature(self, classFeatures: Dict):
        setFeatures = {}
        for key, item in classFeatures.items():
            setFeaturesTemp = np.zeros((1, len(self.featuresIndex)))
            for Features in item:
                setFeaturesTemp += Features
            # 无拉普拉斯修正
            # setFeaturesTemp = setFeaturesTemp / (len(item))  # 除以文件数
            # setFeaturesTemp += 0.000000000000001  # 去0
            # 优化后的拉普拉斯修正(0.0000000000001)越小精度越高
            setFeaturesTemp = (setFeaturesTemp / len(item))
            setFeatures[key] = setFeaturesTemp
        return setFeatures
        # 预测

    def Prediction(self, testSet):
        preClass = []
        for item in testSet:
            Features = self._MakeFeature(item)
            preClass.append(self._toPrediction(Features))
        return preClass

    # 预测单个,不能调用
    def _toPrediction(self, Features):
        minInfo = ["", -sys.maxsize]
        for key, setFeatures in self.calculateModel.items():
            weight = self.classP[key] * np.sum(
                np.log(np.abs(setFeatures + Features - 1.0).clip(min=1 / sys.maxsize)))  # P(A/B)正比于P(A)*P(B/A)
            # 不乘P(A)效果更好,乘P(A)可能是考虑样本不均匀且大样本覆盖面比较广,只有样本显著差异时才可以预测为小样本
            # weight = np.sum(np.log(np.abs(setFeatures + Features - 1)))
            if weight > minInfo[1]:
                minInfo = (key, weight)
        return minInfo[0]
