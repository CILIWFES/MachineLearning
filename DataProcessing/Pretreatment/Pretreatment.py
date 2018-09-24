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
        stopList = self.readFile(GLOCT.SUPPORT_PATH + stopFolder, stopFileName).replace(" ", "").splitlines()
        stopList.append(" ")
        stopList.append("")
        stopList.append("\ufeff")
        stopSet = set(stopList)
        # 保存原始文件
        self.saveFile(GLOCT.SUPPORT_PATH + stopFolder, stopFileName, "\n".join(stopSet))
        # 进行序列化
        ORM.writePickle(GLOCT.SUPPORT_PATH + stopFolder + stopBunchName, stopSet)
        return stopSet

    # 保存文件
    def saveFile(self, savePath, fileName, content):
        if not os.path.exists(savePath):
            os.makedirs(savePath)  # 若不存在则创建目录
        content = content.encode(encoding='utf-8')  # 解码为字节码
        fp = open(savePath + fileName, "wb")
        fp.write(content)
        fp.close()

    # 读取文件
    def readFile(self, classPath, fileName):
        fp = open(classPath + fileName, "rb")
        content = fp.read()
        content = content.decode(encoding='utf-8')  # 解码为字符码
        fp.close()
        return content

