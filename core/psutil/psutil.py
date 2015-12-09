#! /user/bin/python
# coding:UTF-8
from .windows_h import *

# 通过查看TlHelp32.h中的PROCESSENTRY32结构体
# 得知th32DefaultHeapID类型为 ulong
# 在32bit中为4字节 在64bit中为8字节
def process_list():
    hProcessSnap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if hProcessSnap == INVALID_HANDLE_VALUE:
        GetLastError('CreateToolhelp32Snapshot')
        return
    pe32 = PROCESSENTRY32()
    pe32.dwSize = SIZEOF(PROCESSENTRY32)
    if kernel32.Process32First(hProcessSnap, BYREF(pe32)) == 0:
        GetLastError('Process32First')
        kernel32.CloseHandle(hProcessSnap)
        return
    kernel32.Process32Next(hProcessSnap, BYREF(pe32))
    while True:
        yield pe32
        # 注意Process32Next在Win32 API中的返回值为TRUE或FALSE
        # 在Python中不等价于True或False对象
        # kernel32.Process32Next(hProcessSnap, BYREF(pe32)) is False 类型错误
        if kernel32.Process32Next(hProcessSnap, BYREF(pe32)) == 0:
            break
    kernel32.CloseHandle(hProcessSnap)

def exist_process(proc_name):
    # 一定要转换成bytes
    proc_name = proc_name.encode()
    for p in process_list():
        if p.szExeFile == proc_name:
            return True
    return False

def kill_pid(pid):
    #for child_pid in get_child_pid(pid):
    #    kill_pid(child_pid)
    hProcess = kernel32.OpenProcess(PROCESS_TERMINATE, FALSE, pid)
    if hProcess == 0:
        GetLastError('OpenProcess')
        return
    if kernel32.TerminateProcess(hProcess, 0) == 0:
        GetLastError('TerminateProcess')
    kernel32.CloseHandle(hProcess)

def get_proc_pid(proc_name):
    proc_name = proc_name.encode()
    for p in process_list():
        if p.szExeFile == proc_name:
            yield p.th32ProcessID

def kill_process(proc_name):
    for pid in get_proc_pid(proc_name):
        kill_pid(pid)

def load(command_line, show_window=True):
    pi = PROCESS_INFORMATION()
    si = STARTUPINFO()
    si.cb = SIZEOF(si)
    if not show_window:
        si.dwFlags = 0x1
        si.wShowWindow = 0x0
    command_line = command_line.encode('ascii')
    if not kernel32.CreateProcessA(0,command_line,0, 0, 0, CREATE_NEW_CONSOLE, 0, 0, BYREF(si), BYREF(pi)):
        GetLastError('CreateProcessA')
        return False
    kernel32.CloseHandle(pi.hThread)
    kernel32.CloseHandle(pi.hProcess)
    return True

def GetLastError(func):
    print('[-P-]: %s is Failed. GetLastError is %s.' % (func, kernel32.GetLastError()))