class SortList:
    DataIndex = 0
    ValueIndex = DataIndex + 1

    # 最小模式
    MIN = 1
    # 最大模式
    MAX = -1
    INSERTBEFORE = 1
    INSERTAFTER = INSERTBEFORE + 1

    # 列表查找
    SEQUENTIALSEARCH = 0
    # 插值查找
    INTERPOLATIONSEARCH = 1
    # 二分查找
    BINARYSEARCH = 2

    def __init__(self, searchType=BINARYSEARCH, getValFunc=None, mergeFunc=None, cntsLimit=None, model=MIN,
                 inserOrder=None):
        self._lst = list()
        self._getValFunc = getValFunc
        if not self._getValFunc:
            self._getValFunc = self.__getDefalutValue

        self.mergeFunc = mergeFunc
        # 允许合并就不需要模式了
        if mergeFunc is not None:
            inserOrder = None

        # 插前插后
        self.inserOrder = inserOrder
        # 数量限制
        self.cntsLimit = cntsLimit

        # 数组排序模式
        self.model = model

        self.mergeIndex = None
        # 确定查找方法
        if searchType == SortList.BINARYSEARCH:
            self.searchFunction = self.binarySearch
        elif searchType == SortList.INTERPOLATIONSEARCH:
            self.searchFunction = self.interpolationSearch
        else:
            self.searchFunction = self.sequentialSearch

    def put(self, data, val=None):
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

        # 查询
        inx = self.searchFunction(val)

        # 判断合并信号
        if self.mergeIndex is not None:
            self.mergeFunc(data, self._lst[self.mergeIndex][SortList.DataIndex])
        else:
            self._lst.insert(inx, dataBunch)

        # 大于数量限制
        if self.cntsLimit is not None and len(self._lst) > self.cntsLimit:
            self._lst.pop(-1)

    # 顺序搜索
    def sequentialSearch(self, targetValue):
        afterFlag = False
        index = 0
        for index, item in enumerate(self._lst):
            val = item[SortList.ValueIndex]
            if val > targetValue and self.model == SortList.MIN:
                return index
            elif val < targetValue and self.model == SortList.MAX:
                return index
            elif val == targetValue:
                if afterFlag or self.inserOrder == SortList.INSERTAFTER:
                    afterFlag = True
                else:
                    return index
            else:
                if afterFlag:
                    return index
        return index + 1

    # 二分查找
    def binarySearch(self, targetValue) -> int:

        minIndex = 0
        maxIndex = len(self._lst) - 1
        inx = 0
        while maxIndex >= minIndex:
            inx = self._binaryJump(minIndex, maxIndex)
            val = self._lst[inx][SortList.ValueIndex]
            dir = self._directionSelection(val, inx, targetValue, minIndex, maxIndex)
            if dir < 0:
                maxIndex = inx - 1
            elif dir > 0:
                minIndex = inx + 1
            else:
                if val > targetValue:
                    return inx if self.model == SortList.MIN else inx + 1
                elif val < targetValue:
                    return inx if self.model == SortList.MAX else inx + 1
                else:
                    return inx

        return inx

    # 插值查找
    def interpolationSearch(self, targetValue):
        minIndex = 0
        maxIndex = len(self._lst) - 1
        inx = 0
        while maxIndex >= minIndex:
            inx = self._interpolationJump(minIndex, maxIndex, targetValue)
            val = self._lst[inx][SortList.ValueIndex]
            dir = self._directionSelection(val, inx, targetValue, minIndex, maxIndex)
            if dir < 0:
                maxIndex = inx - 1
            elif dir > 0:
                minIndex = inx + 1
            else:
                if val > targetValue:
                    return inx if self.model == SortList.MIN else inx + 1
                elif val < targetValue:
                    return inx if self.model == SortList.MAX else inx + 1
                else:
                    return inx
        return inx

    def _binaryJump(self, minIndex, maxIndex):
        inx = (maxIndex + minIndex) // 2
        return inx

    def _interpolationJump(self, minIndex, maxIndex, val):
        maxVal = self._lst[maxIndex][SortList.ValueIndex]
        minVal = self._lst[minIndex][SortList.ValueIndex]
        if maxVal == minVal:
            if val > maxVal:
                return minIndex if self.model == SortList.MIN else maxIndex
            elif val > maxVal:
                return maxIndex if self.model == SortList.MIN else minIndex
            else:
                return maxIndex if self.inserOrder == SortList.INSERTAFTER else minIndex

        inx = minIndex + (maxIndex - minIndex) * (val - minVal) // (maxVal - minVal)
        if inx > maxIndex:
            return maxIndex
        elif inx < minIndex:
            return minIndex
        return inx

    def _directionSelection(self, val, valIndex, targetVal, minIndex, maxIndex):
        if targetVal < val:
            if self.model == SortList.MIN:
                step = -1
                inserOrder = SortList.INSERTAFTER
            else:
                step = 1
                inserOrder = SortList.INSERTBEFORE

            nextValue = self._nextIndexVal(valIndex, step, minIndex, maxIndex)
            if nextValue is None:
                return 0
            elif targetVal > nextValue:
                return 0
            elif targetVal == nextValue and (self.inserOrder is None or self.inserOrder == inserOrder):
                # 产生合并信号
                self.makeMergeIndex(valIndex)
                # 找到
                return 0
            else:
                # 向右搜索,超出列表表示找到
                return step

        elif targetVal > val:
            if self.model == SortList.MIN:
                step = 1
                inserOrder = SortList.INSERTBEFORE

            else:
                step = -1
                inserOrder = SortList.INSERTAFTER

            nextValue = self._nextIndexVal(valIndex, step, minIndex, maxIndex)
            if nextValue is None:
                return 0
            elif targetVal < nextValue:
                return 0
            elif targetVal == nextValue and (self.inserOrder is None or self.inserOrder == inserOrder):
                # 产生合并信号
                self.makeMergeIndex(valIndex)
                # 找到
                return 0
            else:
                # 向右搜索,超出列表表示找到
                return step
        else:
            # 产生合并信号
            self.makeMergeIndex(valIndex)

            if self.inserOrder == SortList.INSERTAFTER:
                nexVal = self._nextIndexVal(valIndex, 1, minIndex, maxIndex)
                if nexVal is None or nexVal != targetVal:
                    return 0
                else:
                    return 1
            elif self.inserOrder == SortList.INSERTBEFORE:
                nexVal = self._nextIndexVal(valIndex, -1, minIndex, maxIndex)
                if nexVal is None or nexVal != targetVal:
                    return 0
                else:
                    return -1
            else:
                return 0

    def _nextIndexVal(self, index, step, minIndex, maxIndex):
        if index + step <= maxIndex and index + step >= minIndex:
            return self._lst[index + step][SortList.ValueIndex]
        else:
            return None

    # 产生合并信号
    def makeMergeIndex(self, valIndex):
        if self.mergeFunc is not None:
            self.mergeIndex = valIndex

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
