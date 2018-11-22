import numpy as np

# https://www.cnblogs.com/haiyan123/p/8377623.html
arrList1 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 114, 15, 16]]
arrList2 = [[2, 3, 4, 5], [6, 7, 8, 9], [10, 11, 12, 13], [14, 115, 16, 17]]

matrix1 = np.mat(arrList1)
matrix2 = np.mat(arrList2)
arrays1 = np.array(arrList1)
arrays2 = np.array(arrList2)
print("matrix1:", matrix1)
print(type(matrix1))
print("arrays1:", arrays1)
print(type(arrays1))

print("---------------开始-------------------")


# 相加
def addNum(str, arr1, num):
    print(str + "addNum:")
    print(arr1 + num)


addNum("数组", arrays1, 5)
addNum("矩阵", matrix1, 5)
print('-------------------------------------------')


# 逐项相加
def addNumpy(str, arr1, arr2):
    print(str + "addNumpy:")
    print(arr1 + arr2)


addNumpy("数组", arrays1, arrays2)
addNumpy("矩阵", matrix1, matrix2)
print('-------------------------------------------')


# arrays是逐项相乘
# matrix是矩阵相乘
def multiplicationNum(str, arr1, num):
    print(str + "multiplicationNum:")
    print(arr1 * num)


multiplicationNum("数组", arrays1, 5)
multiplicationNum("矩阵", matrix1, 5)
print('-------------------------------------------')


# arrays是逐项相乘
# matrix是矩阵相乘
def multiplication(str, arr1, arr2):
    print(str + "multiplication:")
    print(arr1 * arr2)


multiplication("数组", arrays1, arrays2)
multiplication("矩阵", matrix1, matrix2)
print('-------------------------------------------')


# 矩阵相乘
def matrixMultiplication(str, arr1, arr2):
    print(str + "matrixMultiplication:")
    print(np.dot(arr1, arr2))


matrixMultiplication("数组", arrays1, arrays2)
matrixMultiplication("矩阵", matrix1, matrix2)
print('-------------------------------------------')


# 矩阵相乘
def arraysMultiplication(str, arr1, arr2):
    print(str + "arraysMultiplication:")
    print(np.multiply(arr1, arr2))

arraysMultiplication("数组", arrays1, arrays2)
arraysMultiplication("矩阵", matrix1, matrix2)
print('-------------------------------------------')
# np.sqrt(array)                   平方根函数
# np.exp(array)                    e^array[i]的数组
# np.abs/fabs(array)               计算绝对值
# np.square(array)                 计算各元素的平方 等于array**2
# np.log/log10/log2(array)         计算各元素的各种对数
# np.sign(array)                   计算各元素正负号
# np.isnan(array)                  计算各元素是否为NaN
# np.isinf(array)                  计算各元素是否为NaN
# np.cos/cosh/sin/sinh/tan/tanh(array) 三角函数
# np.modf(array)                   将array中值得整数和小数分离，作两个数组返回
# np.ceil(array)                   向上取整,也就是取比这个数大的整数
# np.floor(array)                  向下取整,也就是取比这个数小的整数np
# np.rint(array)                   四舍五入
# np.trunc(array)                  向0取整
# np.cos(array)                    正弦值
# np.sin(array)                    余弦值
# np.tan(array)                    正切值




print(np.modf(arrays1))
print(np.sign(arrays1))
print(np.trunc(arrays1))