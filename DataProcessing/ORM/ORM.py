import pickle

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


