class DecisionTree:
    def __init__(self):
        pass


class DecisionNode:
    def __init__(self, parent, key, branch, nodeName):
        # 节点名字
        self.nodeName = nodeName
        # 节点索引,定位关键字
        self.key = key
        # 分支字典{dataValue:nextNode}
        self.branch: dict = branch
