from DataProcessing import *
from Global import *
from Analysis.PerformanceMeasure import *
import os


class TextCategorization:
    TrainSearch = GLOCT.SUPPORT_PATH + "TextCategorization/trainSet/"
    TrainJieSearch = GLOCT.SUPPORT_PATH + "TextCategorization/trainSet_Jieba/"
    LoadPah = GLOCT.SUPPORT_PATH + "TextCategorization/Pickle/"

    def __init__(self, fileName="temp.dat", bunchSize=10, cbts="h"):
        self.fileName = fileName
        self.fileInfo = ORM.autoSearch(TextCategorization.TrainSearch)
        self.trainSet = []
        self.trainClass = []
        trainSet = []
        for info in self.fileInfo:
            dir = info[0]
            fileName = info[1]
            self.trainClass.append(dir)
            trainSet.append(Pretreatment.autoJieba(TextCategorization.TrainJieSearch + dir + "\\", fileName,
                                                   TextCategorization.TrainSearch + dir + "\\"))
        # 去除停用词
        trainSet = [Pretreatment.filterWord(item) for item in trainSet]

        # 获取训练集合(不能用自助法)
        self.bunchs = CBTS.makeSet(trainSet, self.trainClass, cbts, bunchSize)

    def _Classification(self, bunch, Classification, performanceModel=False, **key):
        classification = None
        if performanceModel and os.path.exists(self.LoadPah + self.fileName):
            classification = Classification.LoadPickle(self.LoadPah + self.fileName)
        else:
            MPoint.setPoint()
            classification = Classification()
            classification.fit(bunch.trainSet,
                               bunch.trainClass)  # [words1,words2,.........,words3],[class1,class2,......,classn]
            MPoint.showPoint()

        if performanceModel:
            classification.SavePickle(self.LoadPah, self.fileName)

        MPoint.setPoint()
        preClass = classification.Prediction(bunch.testSet, **key)  # [words1,words1,.........,words1]
        MPoint.showPoint("预测")

        return preClass, bunch.testClass

    def Start(self, Classification, performanceModel=False, loops=1, **key):
        preClass = []
        realClass = []
        for times, bunch in enumerate(self.bunchs):
            if loops == times:
                break
            print("第", times + 1, "次")
            # [preclass1,preclass2,......,preclassn],[class1,class2,......,classn]
            preClassTemp, realClassTemp = self._Classification(bunch, Classification,
                                                               performanceModel,
                                                               **key)
            preClass.extend(preClassTemp)
            realClass.extend(realClassTemp)

        perM = PerM()
        perM.fit(preClass, realClass)
        perM.printPRFData()
