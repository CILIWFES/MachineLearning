import datetime
import random
from collections import Counter
import numpy as np

# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)


print("Python学习测试程序")

print("""运行开始
-------------------------------------------------------------------------------------\n""")
startTime = datetime.datetime.now()  # 起始时间

###################################################################################################################

test1 = "1"
test2 = "2"
test3 = "3"
test4 = "4"
test5 = "5"
test6 = "6"
from Analysis.JudgeClass.JudegeClass import JudegeClass

judege = JudegeClass()
judege.Judege([test1, test3, test2, test3, test4], [test1, test4, test1, test3, test2])
judege.printData()
judege.showFigure()

###################################################################################################################
endTime = datetime.datetime.now()  # 终止时间

print("""\n-------------------------------------------------------------------------------------
运行结束
运行时间:""", endTime.microsecond - startTime.microsecond, "纳秒,即", (endTime - startTime).total_seconds(), "秒")
