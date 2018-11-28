class SortList:
    # 数据坐标
    DataIndex = 0
    # 值坐标
    ValueIndex = DataIndex + 1

    # 最小模式
    MIN = 1
    # 最大模式
    MAX = -1
    # 后插入
    INSERTBEFORE = 1
    # 前插入
    INSERTAFTER = INSERTBEFORE + 1

    # 列表查找
    SEQUENTIALSEARCH = 0
    # 插值查找
    INTERPOLATIONSEARCH = 1
    # 二分查找
    BINARYSEARCH = 2

    # 初始化
    # searchType: 搜索类型,二分法/插值/顺序  ,默认二分法
    # getValFunc:用于Val值方法,为空去默认方法
    # mergeFunc: 合并方法,为空表示不合并
    # cntsLimit: 长度限制
    # model: 排序模式,MIN表示从小到大,MAX表示从大到小
    # inserOrder: 插入地区,前插入/后插入/随意插入
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

    # 将元素加入列表中
    def put(self, data, val=None):
        # val为空转化Val
        if not val:
            val = self._getValFunc(data)
        # 长度限制开启,且将要插入的值在长度之外不插入
        # 注意当长度与限制长度相等时必须进入下列流程进行判断(过滤值处于范围之外的情况)
        if self.cntsLimit is not None and len(self._lst) > self.cntsLimit:
            if val > self.getMaxVal() \
                    and self.model == SortList.MIN \
                    :
                return False
            elif val < self.getMinVal() \
                    and self.model == SortList.MAX:
                return False
            # 注意,相等时有可能会合并,有可能有前插入和后插入的情况需要分析

        # 数据节点
        dataNode = [None, None]
        dataNode[SortList.DataIndex] = data
        dataNode[SortList.ValueIndex] = val

        # 查询插入坐标
        inx = self.searchFunction(val)

        # 判断是否合并
        if self.mergeIndex is not None:
            self.mergeFunc(data, self._lst[self.mergeIndex][SortList.DataIndex])
        else:
            # 在index前插入数据
            self._lst.insert(inx, dataNode)

        # 大于数量限制,删减最后一个
        if self.cntsLimit is not None and len(self._lst) > self.cntsLimit:
            self._lst.pop(-1)
            return False

        return True

    # 顺序搜索,查询出适合的坐标,在坐标左端插入目标值
    def sequentialSearch(self, targetValue):
        # 由于遍历值 相等且后插入元素
        afterFlag = False
        index = 0
        for index, item in enumerate(self._lst):
            val = item[SortList.ValueIndex]
            # 最小值模式,目标在当前左边,返回下标
            if val > targetValue and self.model == SortList.MIN:
                return index
            # 最大值模式,目标在当前右边,返回下标
            elif val < targetValue and self.model == SortList.MAX:
                return index
            # 相等
            elif val == targetValue:
                # 当前是后插入,或者后插入选项已经开启(写前面是为了节省效率,虽然没差多少)
                if afterFlag or self.inserOrder == SortList.INSERTAFTER:
                    afterFlag = True
                else:
                    return index
            else:
                # 非上述三种情况,检查后插入相等开关是否开启(判断是否找到相同元素尾部)
                if afterFlag:
                    return index
        return index + 1

    # 二分查找,查询出适合的坐标,在坐标左端插入目标值
    def binarySearch(self, targetValue) -> int:

        minIndex = 0
        maxIndex = len(self._lst) - 1
        inx = 0
        # 判断是否退出
        while maxIndex >= minIndex:
            # 二分跳跃(2,1的类似情况无法跳跃到出来,下面必须处理)
            inx = self._binaryJump(minIndex, maxIndex)
            # 当前值,用于下一步判断
            val = self._lst[inx][SortList.ValueIndex]
            # 下一步跳跃方向,有考虑  前插入后插入,最大/小值模式
            dir = self._directionSelection(val, inx, targetValue, minIndex, maxIndex)
            # 根据方向处理最大最小值
            if dir < 0:
                # -1是为了跳出循环
                maxIndex = inx - 1
            elif dir > 0:
                # +1 也是为了跳出循环
                minIndex = inx + 1
            else:
                # 相等表示返回,但是这不代表结束,还需要判断(又可能是不存在的值)
                return self.selectByDirection(val, targetValue, inx, inx + 1)

        return inx

    # 插值查找,查询出适合的坐标,在坐标左端插入目标值
    def interpolationSearch(self, targetValue):
        minIndex = 0
        maxIndex = len(self._lst) - 1
        inx = 0
        # 判断是否退出
        while maxIndex >= minIndex:
            # 插值跳跃(2,1的类似情况无法跳跃到出来,下面必须处理)
            inx = self._interpolationJump(minIndex, maxIndex, targetValue)
            # 当前值,用于下一步判断
            val = self._lst[inx][SortList.ValueIndex]
            # 下一步跳跃方向,有考虑  前插入后插入,最大/小值模式
            dir = self._directionSelection(val, inx, targetValue, minIndex, maxIndex)
            # 根据方向处理最大最小值
            if dir < 0:
                # -1是为了跳出循环
                maxIndex = inx - 1
            elif dir > 0:
                # +1 也是为了跳出循环
                minIndex = inx + 1
            else:
                # 相等表示返回,但是这不代表结束,还需要判断(又可能是不存在的值)
                return self.selectByDirection(val, targetValue, inx, inx + 1)
        return inx

    # 二分跳跃,返回元素中位(偏小位)
    def _binaryJump(self, minIndex, maxIndex):
        # 二分法
        inx = (maxIndex + minIndex) // 2
        return inx

    def _interpolationJump(self, minIndex, maxIndex, val):
        # 获取状态值
        maxVal = self._lst[maxIndex][SortList.ValueIndex]
        minVal = self._lst[minIndex][SortList.ValueIndex]
        # 相等为了避免/0的异常
        if maxVal == minVal:
            return self.selectByDirection(val, minVal, minIndex, maxIndex)
        # 插值索引
        inx = int(minIndex + (maxIndex - minIndex) * (val - minVal) // (maxVal - minVal))

        # 越过范围,可以终止
        if inx > maxIndex:
            return maxIndex
        elif inx < minIndex:
            return minIndex
        # 正常流程,跳转目标
        return inx

    # 当插入点为当前坐标时,根据当前值与目标值判断插入节点左/右
    def selectByDirection(self, val, targetValue, leftInx, rightInx):
        #  目标在当前左边,最小值模式返回当前值,最大值模式返回当前值右边一个元素(最大值插在右边)
        if val > targetValue:
            return leftInx if self.model == SortList.MIN else rightInx
        elif val < targetValue:
            #  目标在当前右边,最大值模式返回当前值,最小值模式返回当前值右边一个元素(最小值插在右边)
            return leftInx if self.model == SortList.MAX else rightInx
        else:
            # 根据插入点选择,None无需关心
            return rightInx if self.inserOrder == SortList.INSERTAFTER else leftInx

    # 方向选择,向左跳跃还是向右跳跃
    def _directionSelection(self, val, valIndex, targetVal, minIndex, maxIndex):
        if targetVal < val:
            # 最小值:当前值在目标值右边
            if self.model == SortList.MIN:
                # 向左搜索,后插入有退出循环的希望
                step = -1
                inserOrder = SortList.INSERTAFTER
            else:
                # 最大值在当前值在目标左边
                # 向右搜索,前插入有退出循环的希望
                step = 1
                inserOrder = SortList.INSERTBEFORE
            # 通过步长获取下/上一个目标值
            nextValue = self._nextIndexVal(valIndex, step, minIndex, maxIndex)
            # 越界,判定不存在
            if nextValue is None:
                return 0
            # 大于下一个值,说明在发现插入点,直接返回插入点坐标,上一层判断到底输入哪一个插入点(左插入/右插入)
            elif targetVal > nextValue:
                return 0
            # 相等,且插入模式相符合
            elif targetVal == nextValue and (self.inserOrder is None or self.inserOrder == inserOrder):
                # 产生合并信号
                self.makeMergeIndex(valIndex)
                # 找到
                return 0
            else:
                # 返回搜索方向
                return step

        elif targetVal > val:
            # 最小值:当前值在目标值左边
            if self.model == SortList.MIN:
                step = 1
                inserOrder = SortList.INSERTBEFORE

            else:
                # 最大值在当前值在目标右边
                step = -1
                inserOrder = SortList.INSERTAFTER
            # 与上面类似
            nextValue = self._nextIndexVal(valIndex, step, minIndex, maxIndex)
            if nextValue is None:
                return 0
            # 这里不同
            elif targetVal < nextValue:
                return 0

            elif targetVal == nextValue and (self.inserOrder is None or self.inserOrder == inserOrder):
                # 产生合并信号
                self.makeMergeIndex(valIndex)
                # 找到
                return 0
            else:
                # 返回搜索方向
                return step
        else:
            # 相等,需要判断插入模式与是否合并

            # 产生合并信号,退出下面无意义的过程
            if self.mergeFunc is not None:
                self.mergeIndex = valIndex
                return 0

            # 判断是否需要再次跳跃到相同元素尾/头部
            if self.inserOrder == SortList.INSERTAFTER:
                # 尾插入模式,向后
                step = 1
            elif self.inserOrder == SortList.INSERTBEFORE:
                # 头插入模式,向前
                step = -1
            else:
                return 0

            nexVal = self._nextIndexVal(valIndex, step, minIndex, maxIndex)
            # 越界,或者找到目标值
            if nexVal is None or nexVal != targetVal:
                return 0
            else:
                # 没找到继续向后搜索
                return step

    # 获取范围内下/上一个元素的value值
    # 若超标,返回None
    def _nextIndexVal(self, index, step, minIndex, maxIndex):
        # 下/上一个元素的value是否在范围内
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
