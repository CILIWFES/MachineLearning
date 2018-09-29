import pickle
import os


class ORM:
    # 写入对象的序列化
    def writePickle(self, path, object):
        fileObj = open(path, "wb")
        pickle.dump(object, fileObj)
        fileObj.close()

    # 读取对象的序列化
    def loadPickle(self, path):
        fileObj = open(path, "rb")
        object = pickle.load(fileObj)
        fileObj.close()
        return object

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
        content = content.decode(encoding='utf-8').strip()  # 解码为字符码
        fp.close()
        return content
        # 读取文件

    #  通过父文件(一级)价自动搜索,二级类别与类别下的文件(三级)
    # seachPath="xxx/ss/"
    def autoSearch(self, seachPath):
        fileinfo=[]
        cateList = os.listdir(seachPath)
        for mydir in cateList:
            classPath = seachPath + mydir + '/'
            fileList = os.listdir(classPath)
            for fileName in fileList:
                fileinfo.append((mydir,fileName))
        return fileinfo
