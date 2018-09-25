import os
from Global import *
from DataProcessing.ORM import *


# 规定,一行表示一组数据
# 数据预处理,读取数据.并调用停用词
class Pretreatment:

    # 获取停用词文本集合（Set）
    def getStopWordsSet(self):
        stopFolder = GLOCF.getConfig(GLOCT.STOPWORDS_CONFIG_SECTION, GLOCT.SAVE_FOLDER_CONFIG)
        stopBunchName = GLOCF.getConfig(GLOCT.STOPWORDS_CONFIG_SECTION, GLOCT.SAVE_BUNCHNAME_CONFIG)

        # 若已经存在则不创建，直接读取
        if os.path.exists(GLOCT.SUPPORT_PATH + stopFolder + stopBunchName):
            return ORM.loadPickle(GLOCT.SUPPORT_PATH + stopFolder + stopBunchName)
        # 先处理一下
        stopFileName = GLOCF.getConfig(GLOCT.STOPWORDS_CONFIG_SECTION, GLOCT.SAVE_FILENAME_CONFIG)
        stopList = ORM.readFile(GLOCT.SUPPORT_PATH + stopFolder, stopFileName).replace(" ", "").splitlines()
        stopList.append(" ")
        stopList.append("")
        stopList.append("\ufeff")
        stopSet = set(stopList)
        # 保存原始文件
        ORM.saveFile(GLOCT.SUPPORT_PATH + stopFolder, stopFileName, "\n".join(stopSet))
        # 进行序列化
        ORM.writePickle(GLOCT.SUPPORT_PATH + stopFolder + stopBunchName, stopSet)
        return stopSet



