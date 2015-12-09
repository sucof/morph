#! /user/bin/python
# coding:UTF-8

import time
import re
import os

import config
from core import psutil, file

def GetCrashHash(logPath):
    content = file.ReadFromFile(logPath)
    try:
        crash_exploitable = re.search("Exploitability Classification: \w+", content).group().replace("Exploitability Classification: ", "", 1)
        crash_type = re.search("Short Description: \w+", content).group().replace("Short Description: ", "", 1)
        crash_md5 = re.search("Hash=0x\w+\.0x\w+", content).group().replace("Hash=", "", 1)
        return ("%s_%s_%s" % (crash_exploitable, crash_type, crash_md5))
    except: # 若解析log不成功则直接以当前时间命名该Crash
        return ("CRASH_%s" % time.time())


def handle_crash_proc( ):
    # 结束Debugger和浏览器进程
    time.sleep(5)  # 给Symbols加载留足够的时间
    config.TerminateProc()
    # 得到当前Crash序号
    crash_num = config.MOR_LAST_COMPLETE_VECOTR + 1
    crash_num_name = "%d%s" % (crash_num, config.MOR_FUZZER_SUFFIX)
    vectorCrashPath = os.path.join(config.MOR_VECTORS_FOLDER, crash_num_name)
    # 读取log信息
    debuggerLogPath = config.MOR_DEBUGGER[config.MOR_PLATFORM]['log']
    crashHash = GetCrashHash(debuggerLogPath)
    # 保存当前样本和当前log
    dstCrashPath = os.path.join(config.MOR_CRASHES_FOLDER, crashHash + config.MOR_FUZZER_SUFFIX)
    dstLogPath = os.path.join(config.MOR_CRASHES_FOLDER, crashHash + config.MOR_DBGLOG_SUFFIX)
    file.SaveFileFromSrcToDst(vectorCrashPath, dstCrashPath)
    file.SaveFileFromSrcToDst(debuggerLogPath, dstLogPath)
    config.MOR_LAST_COMPLETE_VECOTR += 1
    config.logging_info('M', "Save Crashed Vector %s to %s." % (crash_num_name, crashHash + config.MOR_FUZZER_SUFFIX))

# 将多重循环封装为函数 用Return跳出多重循环分支
def monitor_crash_proc( ):
    monitor_proc = config.MOR_DEBUGGER[config.MOR_PLATFORM]['proc']
    while True:
        if config.MOR_LAST_COMPLETE_VECOTR >= config.MOR_PRE_VECTORS_NUM-1:
            config.MOR_MONITOR_RUNNING = False
        if config.MOR_MONITOR_RUNNING is False or psutil.exist_process(monitor_proc):
            return

def Watch():
    config.MOR_MONITOR_RUNNING = True
    # 循环检测是否出现崩溃进程
    monitor_crash_proc()
    # 保存当前Crash样本
    if config.MOR_MONITOR_RUNNING is True:
        handle_crash_proc()