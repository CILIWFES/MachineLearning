import os
from Global import *
from DataProcessing.ORM import *
import jieba as jba
from typing import List


# 规定,一行表示一组数据
# 数据预处理,读取数据.并调用停用词
class Pretreatment:
    def __init__(self):
        self.stopSet = self.getStopWordsSet()

    # 获取停用词文本集合（Set）
    def getStopWordsSet(self):
        stopFolder = GLOCF.getConfig(GLOCT.STOPWORDS_CONFIG_SECTION, GLOCT.SAVE_FOLDER_CONFIG)
        stopBunchName = GLOCF.getConfig(GLOCT.STOPWORDS_CONFIG_SECTION, GLOCT.SAVE_BUNCHNAME_CONFIG)

        # 若已经存在则不创建，直接读取
        if os.path.exists(GLOCT.SUPPORT_PATH + stopFolder + stopBunchName):
            return ORM.LoadPickle(GLOCT.SUPPORT_PATH + stopFolder + stopBunchName)
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
        ORM.writePickle(GLOCT.SUPPORT_PATH + stopFolder, stopBunchName, stopSet)
        return stopSet

    # 过滤停用词
    # words传入list[str]
    def filterWord(self, words):
        words = [item for item in words if item not in self.stopSet]
        return words

    # 调用分词,输入字符串返回List
    def jieba(self, word: str) -> list:
        word = word.replace("\t", "").replace("\r", "").replace("\n", "").replace(" ", "")
        words = jba.cut(word)
        return words

    # 先检查分词是否存在,若不存在,自动加载文本分词
    def autoJieba(self, jiebaPath, fileName, fileDir=None):
        jiebaWord: List = None
        # 若已经存在则不创建，直接读取
        if os.path.exists(jiebaPath + fileName):
            jiebaWord = ORM.readFile(jiebaPath, fileName).split(
                GLOCF.getConfig(GLOCT.Segmentation_CONFIG_SECTION, GLOCT.Jieba_Segmentation))
        else:  # 先读取,再分词,再保存,最后返回
            word = ORM.readFile(fileDir, fileName)
            jiebaGen = self.jieba(word)
            jiebaWord = GLOCF.getConfig(GLOCT.Segmentation_CONFIG_SECTION, GLOCT.Jieba_Segmentation).join(jiebaGen)
            ORM.saveFile(jiebaPath, fileName, jiebaWord)
        return jiebaWord
