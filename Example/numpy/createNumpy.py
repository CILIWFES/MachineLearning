import numpy as np

# 1、创建一个长度为10的数组，数组的值都是0
np.zeros(10, dtype=int)

# 2、创建一个3x5的浮点型数组，数组的值都是1
np.ones((3, 5), dtype=float)

# 3、创建一个3x5的浮点型数组，数组的值都是3.14
np.full((3, 5), 3.14)

# 4、创建一个3x5的浮点型数组，数组的值是一个线性序列,从o开始，到20结束，步长为2,（它和内置的range()函数类似
np.arange(0, 20, 2)

# 5、创建一个5个元素的数组，这5个数均匀的分配到0～1
np.linsapace(0, 1, 5)

# 6、创建一个3x3的，在0～1均匀分配的随机数组成的数组
np.random.random(3, 3)

# 7、创建一个3x3的，均值为0，方差为1,正太分布的随即数数组
np.random.normal(0, 1, (3, 3))

# 8、创建一个3x3的，[0,10]区间的随机整形数组
np.random.randint(0, 10, (3, 3))

# 9、创建一个3x3的单位矩阵
np.eye(3)

# 10、创建一个由3个整形数组组成的未初始化的数组,数组的值是内存空间中的任意值
np.empty(3)