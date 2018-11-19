import numpy as np

"""
Numpy matrices必须是2维的,但是 numpy arrays (ndarrays) 可以是多维的（1D，2D，3D····ND）. 
Matrix是Array的一个小的分支，包含于Array。
所以matrix 拥有array的所有特性。
"""
array1 = np.array([[[[7, 8, 99]], [[7, 8, 99]]]])
print(array1.shape)

def firstShow():
    """
    可以看到array和mat还是有所不同的。
    array: 将list直接转换成了数组，包括但不限于一维的list
    mat: 将list中的数据转换成了矩阵
    所以在使用命令tolist进行对array转换后可以转换成原来的样子，对mat类型转换后会和原来有所不同。
    """
    two = [1, 3, 5, 2, 3, 2]
    two1 = np.array(two)
    print(two)  # [1, 3, 5, 2, 3, 2]  type:list
    print(two1)  # [1 3 5 2 3 2]  type:numpy.ndarray
    print(two1.shape)  # (6,)
    print(two1.tolist())  # [1, 3, 5, 2, 3, 2]  type:list
    print(len(two1.tolist()))  # 6
    two2 = np.mat(two)
    print(two2)  # [[1 3 5 2 3 2]]  type:numpy.matrixlib.defmatrix.matrix
    print(two2.shape)  # (1, 6)一维
    print(two2.tolist())  # [[1, 3, 5, 2, 3, 2]]  type:二维list
    print(len(two2.tolist()))  # 1


# firstShow()


"""
在numpy中matrix的主要优势是：相对简单的乘法运算符号。
例如，a和b是两个matrices，那么a*b，就是矩阵积。
"""


def matrixAdvantage():
    print('matrixAdvantage')
    # ; 表示分割
    a = np.mat('4 3; 2 1')
    b = np.mat('1 2; 3 4')
    # temp = np.mat('1 2 3 4') #[[1 2 3 4]]
    print(a)  # [[4 3] [2 1]]
    print('-----------')
    # 因为a是个matrix，所以a**2返回的是a*a，相当于矩阵相乘
    print(a ** 2)  # [[22 15] [10  7]]
    print(b)  # [[1 2] [3 4]]
    temp = a * b
    print(temp)  # [[13 20] [ 5  8]]
    print(type(temp))  # <class 'numpy.matrixlib.defmatrix.matrix'>

    # 逐项相乘
    temp = np.multiply(a, b)
    print(temp)  # [[4 6] [6 4]]

    print('matrixAdvantage')

    """
    matrix和array都可以通过objects后面加.T 得到其转置。
    但是matrix objects 还可以在后面加 .H 得到共轭矩阵, 加 .I 得到逆矩阵。
    """
    print(temp.H)  # [[13  5] [20  8]]
    print(temp.I)  # [[ 2.   -5.  ] [-1.25  3.25]]


matrixAdvantage()

"""
相反的是在numpy里面arrays遵从逐个元素的运算，
所以array：c和d的c * d运算相当于matlab里面的逐项相乘运算。
而矩阵相乘，则需要numpy里面的dot命令
运算符的作用也不一样
"""
def arrayCalculate():
    c = np.array([[4, 3], [2, 1]])
    # 4 3
    # 2 1
    d = np.array([[1, 2], [3, 4]])
    # 1 2
    # 3 4
    print(type(c))  # <class 'numpy.ndarray'>
    print(c * d)  # [[4 6] [6 4]],c与d索引相乘

    # 矩阵相乘，则需要numpy里面的dot命令 :
    print(np.dot(c, d))  # [[13 20] [5  8]]

    # c**2相当于，c中的元素逐个求平方。
    print(c ** 2)  # [[16  9] [4  1]]<-[[4**2, 3**2], [2**2, 1**2]]


# arrayCalculate()

"""
问题就出来了，如果一个程序里面既有matrix 又有array，会让人脑袋大。
但是如果只用array，你不仅可以实现matrix所有的功能，还减少了编程和阅读的麻烦。
当然你可以通过下面的两条命令轻松的实现两者之间的转换：np.asmatrix和np.asarray
"""
def Conversion():
    c = np.array([[4, 3], [2, 1]])
    a = np.mat('4 3; 2 1')
    print('---------------------------')
    print(type(a))
    print(a)
    a = np.asarray(a)
    print(a)
    print(type(a))
    print('---------------------------')
    print(type(c))
    print(c)
    c = np.asmatrix(c)
    print(c)
    print(type(c))


Conversion()

"""
matrix是array的分支，matrix和array在很多时候都是通用的，
你用哪一个都一样。但这时候，官方建议大家如果两个可以通用，
那就选择array，因为array更灵活，速度更快，很多人把二维的array也翻译成矩阵。 
但是matrix的优势就是相对简单的运算符号，比如两个矩阵相乘，
就是用符号*，但是array相乘不能这么用，得用方法.dot() 
array的优势就是不仅仅表示二维，还能表示3、4、5…维，
而且在大部分Python程序里，array也是更常用的。
"""
