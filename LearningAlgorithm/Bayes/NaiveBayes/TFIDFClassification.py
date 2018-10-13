import numpy as np
from typing import List, Dict
from DataProcessing.ORM import *

import sys


class TFIDF:

    def SavePickle(self, path, fileName):
        ORM.writePickle(path, fileName, self)

    @staticmethod
    def LoadPickle(path):
        return ORM.LoadPickle(path)

    def __init__(self):
        # 特征袋模型,{name:矩阵},每个分类都有自己的特征袋
        self.TfIdf = {}
        # 特征名索引
        self.featureIndex = {}
        # 类别概率
        self.classList = []
        self.classIndex = {}

    # trainSet训练集(list)
    def fit(self, trainSet: List, trainClass):
        # 对类型进行归类,并计算概率
        self.classList, self.classIndex = self._BuildCategoryIndex(trainClass)
        # 建立特征袋索引
        self.featureIndex = self._BuildFeatureIndex(trainSet)
        # 构建特征袋类别-文件特征袋dict
        classFeatures = self._BuildClassFeature(trainSet, trainClass)
        # 计算文件预测特征袋
        self.TfIdf = self._BuildTfIdfFeature(classFeatures)

    # 建立类别索引
    def _BuildCategoryIndex(self, trainClass):
        classList = list(set(trainClass))
        classIndex = {key: index for index, key in enumerate(classList)}
        return classList, classIndex

    # 根据特征名,生成量化特征字典
    def _BuildFeatureIndex(self, trainSet):
        setTemp = set()
        avgFile = 0
        for item in trainSet:
            avgFile += len(item)
            itemSet = set(item)
            setTemp.update(itemSet)
        featureIndex = {name: index for index, name in enumerate(setTemp)}
        return featureIndex

    # 量化特征
    def _BuildFeatureDict(self, features: List):
        # 新建初始长度为特征典表的矩阵
        lst = np.zeros((1, len(self.featureIndex)))
        for feature in features:
            if feature in self.featureIndex:
                lst[0, self.featureIndex[feature]] += 1
        return lst[0]

    # 构建特征袋模型
    def _BuildClassFeature(self, trainSet, trainClass):
        classFeatures = {}
        for index, item in enumerate(trainClass):
            featureTemp = trainSet[index]
            feature = self._BuildFeatureDict(featureTemp)
            if item in classFeatures:
                classFeatures[item].append(feature)
            else:
                classFeatures[item] = [feature]
        return classFeatures

    def _IDF(self, classFeatures):
        setFeatures = {}
        IDFClass = {}
        # 总文件频率
        AllSetFeatures = np.zeros((1, len(self.featureIndex)))
        # 总分类频率
        ClassSetFeatures = np.zeros((1, len(self.featureIndex)))
        fileCnt = 0
        for key, item in classFeatures.items():
            features = np.sum(np.mat(item).clip(max=1), axis=0)
            fileCnt += len(item)
            # 转化为特征集模型
            AllSetFeatures = features + AllSetFeatures
            features = [0 if i <= 0 else 1 for i in features.tolist()[0]]
            ClassSetFeatures = features + ClassSetFeatures

        # 书本上是写这个逆文件频率(文件越多越接近0)
        # return np.log(fileCnt / AllSetFeatures)
        # 我做的逆类别频率类别越多越接近0
        # return np.log(len(self.classList) / ClassSetFeatures)

        # 综合1
        # return np.log(np.multiply((fileCnt / AllSetFeatures), (len(self.classList) / ClassSetFeatures)))
        # 综合2
        return np.multiply(np.log((fileCnt / AllSetFeatures)), np.log((len(self.classList) / ClassSetFeatures)))

    def _TF(self, classFeatures):
        TFClass = classFeatures
        for key, item in classFeatures.items():
            features = np.sum(np.mat(item), axis=0)
            features = (features + 1 / np.sum(features)) / np.sum(features)
            TFClass[key] = features
        return TFClass

    # 计算核心
    def _BuildTfIdfFeature(self, classFeatures: Dict):
        TfIdf = {}
        idf = self._IDF(classFeatures)
        tf = self._TF(classFeatures)
        for key, item in tf.items():
            TfIdf[key] = np.multiply(item, idf)
        return TfIdf

    # 预测
    def Prediction(self, testSet):
        preClass = []
        for item in testSet:
            features = self._BuildFeatureDict(item)
            preClass.append(self._PredictionOne(features))
        return preClass

    # 预测单个,不能调用
    def _PredictionOne(self, features):
        features += 1 / np.sum(features)
        minInfo = ["", -sys.maxsize]
        for key, tfIdf in self.TfIdf.items():
            weight = np.sum(np.multiply(features, tfIdf))
            if weight > minInfo[1]:
                minInfo = (key, weight)
        return minInfo[0]
