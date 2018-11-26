class SortList:
    DataIndex = 0
    ValueIndex = DataIndex + 1

    # 最小模式
    MIN = 1
    # 最大模式
    MAX = -1

    def __init__(self, getValFunc=None, mergeFunc=None, cntsLimit=None, model=MIN):
        self._lst = list()
        self._getValFunc = getValFunc
        if not self._getValFunc:
            self._getValFunc = self.__getDefalutValue
        self.mergeFunc = mergeFunc

        # 数量限制
        self.cntsLimit = cntsLimit
        # 数组排序模式
        self.model = model

    def put(self, data, val=None):
        isInser = False
        if not val:
            val = self._getValFunc(data)

        if self.cntsLimit is not None and len(self._lst) > self.cntsLimit:
            if val > self.getMaxVal() \
                    and self.model == SortList.MIN \
                    :
                return
            elif val < self.getMinVal() \
                    and self.model == SortList.MAX:
                return

        dataBunch = [None, None]
        dataBunch[SortList.DataIndex] = data
        dataBunch[SortList.ValueIndex] = val
        # 排序插入
        for index, item in enumerate(self._lst):
            compareVal = item[SortList.ValueIndex]
            if compareVal > val and self.model == SortList.MIN:
                self._lst.insert(index, dataBunch)
                isInser = True
                break
            elif compareVal < val and self.model == SortList.MAX:
                self._lst.insert(index, dataBunch)
                isInser = True
                break
            elif compareVal == val:  # 距离相等判断是否合并
                if self.mergeFunc:  # 开始合并
                    item[SortList.DataIndex] = self.mergeFunc(item[SortList.DataIndex], data)
                else:  # 取消合并
                    self._lst.insert(index, dataBunch)
                isInser = True
                break

        if not isInser:
            self._lst.append(dataBunch)

        # 大于数量限制
        if self.cntsLimit is not None and len(self._lst) > self.cntsLimit:
            self._lst.pop(-1)

    def __getDefalutValue(self, data):
        return data

    def clear(self):
        self._lst.clear()

    def getAllList(self):
        return self._lst

    def getDataList(self):
        return [item[SortList.DataIndex] for item in self._lst]

    def getValList(self):
        return [item[SortList.ValueIndex] for item in self._lst]

    def getMinVal(self):
        return self._lst[0][SortList.ValueIndex]

    def getMinData(self):
        return self._lst[0][SortList.DataIndex]

    def getMaxVal(self):
        return self._lst[-1][SortList.ValueIndex]

    def getMaxData(self):
        return self._lst[-1][SortList.DataIndex]
