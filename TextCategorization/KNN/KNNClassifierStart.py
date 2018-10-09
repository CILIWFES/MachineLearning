from TextCategorization.Bayesian.TF_IDF import *
from DataProcessing import *
from Global import *
from Analysis.PerformanceMeasure import *
import os

print("运行开始")

print("运行开始")

TrainSearch = GLOCT.SUPPORT_PATH + "TextCategorization/TrainSet/"
TrainJieSearch = GLOCT.SUPPORT_PATH + "TextCategorization/TrainSet_Jieba/"

LoadPah = GLOCT.ROOT_PATH + "FileSupport/KNN/KNNClassifier/Pickle/"
FileName = "KNNClassifier.dat"

# 获取训练集合
fileInfo = ORM.autoSearch(TrainSearch)
classSet = []
trainSet = []
for info in fileInfo:
    dir = info[0]
    fileName = info[1]
    classSet.append(dir)
    trainSet.append(Pretreatment.autoJieba(TrainJieSearch + dir + "\\", fileName, TrainSearch + dir + "\\"))
# 去除停用词
trainSet = [Pretreatment.filterWord(item) for item in trainSet]

# 获取训练集合(不能用自助法)
Bunchs = CBTS.makeSet(trainSet, classSet, "h", 10)

print("完成加载,开始执行")
# 性能模式(线上模式开启)
performanceModel = False


