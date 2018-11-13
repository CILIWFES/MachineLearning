import numpy as np

"""
bool_	布尔型数据类型（True 或者 False）
int_	默认的整数类型（类似于 C 语言中的 long，int32 或 int64）
intc	与 C 的 int 类型一样，一般是 int32 或 int 64
intp	用于索引的整数类型（类似于 C 的 ssize_t，一般情况下仍然是 int32 或 int64）
int8	字节（-128 to 127）
int16	整数（-32768 to 32767）
int32	整数（-2147483648 to 2147483647）
int64	整数（-9223372036854775808 to 9223372036854775807）
uint8	无符号整数（0 to 255）
uint16	无符号整数（0 to 65535）
uint32	无符号整数（0 to 4294967295）
uint64	无符号整数（0 to 18446744073709551615）
float_	float64 类型的简写
float16	半精度浮点数，包括：1 个符号位，5 个指数位，10 个尾数位
float32	单精度浮点数，包括：1 个符号位，8 个指数位，23 个尾数位
float64	双精度浮点数，包括：1 个符号位，11 个指数位，52 个尾数位
complex_	complex128 类型的简写，即 128 位复数
complex64	复数，表示双 32 位浮点数（实数部分和虚数部分）
complex128	复数，表示双 64 位浮点数（实数部分和虚数部分）
"""

"""
numpy.dtype(object, align, copy)
object - 要转换为的数据类型对象
align - 如果为 true，填充字段使其类似 C 的结构体。
copy - 复制 dtype 对象 ，如果为 false，则是对内置数据类型对象的引用
"""


def test():
    # 自定义结构类型
    # 每一个()是一个编码格式,name表示第一个别名为name,str,40 表示40位byte类型数组
    # t = np.dtype([('name', str,40), ('numitems', np.int32), ('price', np.float32)])
    # 或者写成这样 S40可以改成U40表示修改编码(没有b)
    # 10 表示int32 10 个数组
    t = np.dtype([('name', 'S40'), ('numitems', 'i4', 10), ('price', 'f4')])  # 生成的array必须是(1,2,3)的类型与参数数量

    # 获取字段类型
    print(t)
    # 使用记录类型创建数组
    # 否则它会把记录拆开
    # ('Butter', 13, 2.72)表示一个单元
    item = np.array([('Meaning of life DVD', 42, 3.14), ('Butter', 13, 2.72)], dtype=t)
    print(item)


# test()


"""
bool	    ?, b1
int8	    b, i1
uint8	    B, u1
int16	    h, i2
uint16	    H, u2
int32	    i, i4
uint32	    I, u4
int64	    q, i8
uint64	    Q, u8
float16	    f2, e
float32	    f4, f
float64	    f8, d
complex64	F4, F
complex128	F8, D
str	        a, S（可以在S后面添加数字，表示字符串长度，比如S3表示长度为三的字符串，不写则为最大长度）
unicode	    U
object	    O
void	    V
--------------------- 
作者：AKA_Johnnie 
来源：CSDN 
原文：https://blog.csdn.net/zhili_wang/article/details/81140282 
"""


def conversion():
    """
    https://www.cnblogs.com/hellcat/p/8711160.html
    """
    # (flexible_dtype, itemsize)第一个大小不固定的参数类型，第二传入大小：
    dt = np.dtype(("V", 10))  # 10位

    dt = np.dtype((str, 10))  # 35字符字符串
    item = np.array("012345678910", dtype=dt)
    print(item)
    print(type(item))
    dt = np.dtype(('U', 5))  # 10字符unicode string
    item = np.array([23467865432, 1, 2, 3, 4, 5, 3245678654, 7, 8, 9, 10], dtype=dt)
    print(item)
    print(type(item))

    # (fixed_dtype, shape)第一个传入固定大小的类型参数，第二参数传入个数
    dt = np.dtype((np.int32, (2, 2)))  # 2*2int子数组([2],[2])
    print('(np.int32, (2, 2))')
    # 举例:
    item = np.array([([12, 12], [55, 56])], dtype=dt)
    print(item)
    dt = np.dtype((np.int32, 2))  # 2*2int子数组([2],[2])
    item = np.array([(12, 12), (55, 56)], dtype=dt)
    print(item)

    dt = np.dtype(('S10', 1))  # 10字符字符串,为1说明不是数组
    item = np.array([("sadas", '87', '8888')], dtype=dt)
    print(item)
    dt = np.dtype(('S10', 2))  # 10字符字符串,为2说明是数组,S不能为中文,U可以中文
    # item = np.array([("sadas", '87', '8888', '8888')], dtype=dt)
    # cannot copy sequence with size 4 to array axis with dimension 2
    item = np.array([("sadas", '87')], dtype=dt)
    item = np.array([("sadas", '87'), ("nochines", '8987')], dtype=dt)
    print(item)

    dt = np.dtype(('i4, f8, f4', (2, 3)))  # 2*3结构子数组
    item = np.array([([5, 0.5, 0.5], [5, 0.5, 0.5])], dtype=dt)
    print(item)

    # 也表示两行三列的F8
    dt = np.dtype(('i4, (2,3)f8, f4', (2, 3)))  # 2*3结构子数组
    item = np.array([([5, 0.5, 0.5], [5, 0.5, 0.5])], dtype=dt)
    print(item)

    # [(field_name, field_dtype, field_shape), …]
    dt = np.dtype([('big', '>i4'), ('little', '<i4')])
    item = np.array([(87, 777)], dtype=dt)
    print(item)

    # u1 是uint8
    dt = np.dtype([('R', 'u1'), ('G', 'u1'), ('B', 'u1'), ('A', 'u1')])
    item = np.array([('1', '2', '4', '4')], dtype=dt)
    print(item)

    # (1,5)把数据转化为[[5,8,7,7,9]]
    dt = np.dtype([('R', 'u1'), ('G', 'u1'), ('B', 'u1'), ('A', '(1,5)i4')])
    item = np.array([('1', '2', '4', [5, 8, 7, 7, 9])], dtype=dt)
    print(item)

    # {‘names’: …, ‘formats’: …, ‘offsets’: …, ‘titles’: …, ‘itemsize’: …}：
    dt = np.dtype({'names': ('Date', 'Close'), 'formats': ('S10', 'f8')})
    item = np.array([('sadas', 0.58755)], dtype=dt)
    print(item)
    dt = np.dtype(
        {'names': ['r', 'b'], 'formats': ['u1', 'u1'], 'offsets': [0, 2], 'titles': ['Red pixel', 'Blue pixel']})
    item = np.array([('1', '2')], dtype=dt)
    print(item)

    # (base_dtype, new_dtype)：
    dt = np.dtype((np.int32, (np.int8, 4)))  # base_dtype被分成4个int8的子数组
    print('(np.int32, (np.int8, 4))')
    item = np.array([(145879)], dtype=dt)
    print(item)
    print(dt)


conversion()
