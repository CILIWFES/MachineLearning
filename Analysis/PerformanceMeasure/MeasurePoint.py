import psutil
import os
import gc
import time
import threading


# info = psutil.virtual_memory()
# print('内存使用：', psutil.Process(os.getpid()).memory_info().rss)
# print('总内存：', info.total)
# print('内存占比：', info.percent)
# print('cpu个数：', psutil.cpu_count())
# 时间/内存度量类
class MeasurePoint:
    def __init__(self):
        self.inital_Time_Occupy = None
        self.RAMThread = None

    def setRAMPoint(self):
        gc.collect()
        if self.RAMThread is None:
            self.RAMThread = RAMThread()
            self.RAMThread.start()
        else:
            raise Exception('标记已经存在')

    def setTimePoint(self):
        if self.inital_Time_Occupy is None:
            self.inital_Time_Occupy = time.clock()
        else:
            raise Exception('标记已经存在')

    def showRAMPoint(self, message="", defaultMsg=" 占用内存:"):
        if self.RAMThread is None:
            raise Exception('RAM标记不存在')
        program_RAM_Occupy = self.RAMThread.getRAM()
        print(message + defaultMsg, program_RAM_Occupy / 1000, "KB/", program_RAM_Occupy / 1000 / 1000, "MB/",
              program_RAM_Occupy / 1000 / 1000 / 1000,
              "GB")
        self.RAMThread = None
        gc.collect()

    def showTimePoint(self, message="", defaultMsg=" 占用时间:"):
        if self.inital_Time_Occupy is None:
            raise Exception('Time标记不存在')
        now_Time_Occupy = time.clock()
        program_Time_Occupy = now_Time_Occupy - self.inital_Time_Occupy
        print(message + defaultMsg, program_Time_Occupy, "秒")
        self.inital_Time_Occupy = None

    def set_Time_RAM_Point(self, isTime=False):
        if isTime:
            self.setTimePoint()
        else:
            self.setRAMPoint()
            self.setTimePoint()

    def show_Time_RAM_Point(self, message="", isTime=False, defaultTime=" 占用时间:", defaultRAM=" 占用内存:"):
        if isTime:
            self.showTimePoint(message, defaultTime)
        else:
            self.showTimePoint(message, " 评估时间:")
            self.showRAMPoint(message, defaultRAM)


# 定时收集内存信息
class RAMThread(threading.Thread):
    SLEEPTIME = 0.0001  # 收集内存信息频率

    def __init__(self):
        super().__init__()
        self._RAMSize = 0
        self._stop = True
        self.process = psutil.Process(os.getpid())

    def run(self):
        old_RAM_Occupy = self.process.memory_info().rss
        while (self._stop):
            now_RAM_Occupy = self.process.memory_info().rss
            program_RAM_Occupy = now_RAM_Occupy - old_RAM_Occupy
            # 判断垃圾没有被回收
            program_RAM_Occupy = 0 if program_RAM_Occupy < 0 else 1 * program_RAM_Occupy
            self._RAMSize += program_RAM_Occupy
            old_RAM_Occupy = now_RAM_Occupy
            time.sleep(RAMThread.SLEEPTIME)

    def getRAM(self):
        self._stop = False
        return self._RAMSize
