import numpy as np


def showAll():
    # 1、创建一个长度为10的数组，数组的值都是0
    arr1 = np.zeros(10, dtype=int)
    print(arr1)
    print(arr1.shape)

    # 2、创建一个3x5的浮点型数组，数组的值都是1
    arr1 = np.ones((3, 5), dtype=float)
    print(arr1)
    print(arr1.shape)

    # 3、创建一个3x5的浮点型数组，数组的值都是3.14
    arr1 = np.full((3, 5), 3.14)
    print(arr1)
    print(arr1.shape)

    # 4、创建一个3x5的浮点型数组，数组的值是一个线性序列,从o开始，到20结束，步长为2,（它和内置的range()函数类似
    arr1 = np.arange(0, 20, 2)
    print(arr1)
    print(arr1.shape)

    # 5、创建一个5个元素的数组，这5个数均匀的分配到0～1
    arr1 = np.linspace(0, 1, 5)
    print(arr1)
    print(arr1.shape)

    # 6、创建一个3x3的，在0～1均匀分配的随机数组成的数组
    arr1 = np.random.random((3, 2))
    print(arr1)
    print(arr1.shape)

    # 7、创建一个3x3的，均值为0，方差为1(概率上),正太分布的随即数数组
    arr1 = np.random.normal(0, 1, (3, 3))
    print(arr1)
    print(arr1.shape)

    # 8、创建一个3x3的，[0,10]区间的随机整形数组
    arr1 = np.random.randint(0, 10, (3, 3))
    print(arr1)
    print(arr1.shape)

    # 9、创建一个3x3的单位矩阵
    arr1 = np.eye(3)
    print(arr1)
    print(arr1.shape)

    # 10、创建一个由3个整形数组组成的未初始化的数组,数组的值是内存空间中的任意值
    arr1 = np.empty(3)
    print(arr1)
    print(arr1.shape)


# showAll()
def test():
    arr1 = np.zeros((5, 5), dtype=int)
    print(arr1)
    print(arr1.shape)

    arr1 = np.full(5, 3.14)
    print(arr1)
    print(arr1.shape)
    arr1 = np.random.normal(0, 1, (3, 30000))
    print(arr1)
    print(arr1.shape)
    print("平均:", np.mean(arr1))
    print("方差:", np.std(arr1))


test()
