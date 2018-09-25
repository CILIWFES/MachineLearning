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
        content = content.decode(encoding='utf-8')  # 解码为字符码
        fp.close()
        return content
