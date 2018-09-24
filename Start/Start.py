import datetime
import random
from collections import Counter
import numpy as np
import os

# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)


print("Python学习测试程序")

print("""运行开始
-------------------------------------------------------------------------------------\n""")
startTime = datetime.datetime.now()  # 起始时间

###################################################################################################################
print(os.getcwd())
print(os.path.abspath(os.path.dirname(__file__)))

print('***获取上级目录***')
print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
print(os.path.abspath(os.path.dirname(os.getcwd())))
print(os.path.abspath(os.path.join(os.getcwd(), "..")))

print('***获取上上级目录***')
print(os.path.abspath(os.path.join(os.getcwd(), "../..")))

###################################################################################################################
endTime = datetime.datetime.now()  # 终止时间

print("""\n-------------------------------------------------------------------------------------
运行结束
运行时间:""", endTime.microsecond - startTime.microsecond, "纳秒,即", (endTime - startTime).total_seconds(), "秒")
