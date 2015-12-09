#! /user/bin/python
# coding:utf-8

import platform
import ctypes

DWORD = ctypes.c_ulong
WORD = ctypes.c_ushort
HANDLE = ctypes.c_void_p
LPVOID = PVOID = ctypes.c_void_p
TCHAR = ctypes.c_char
CHAR = ctypes.c_char
LPSTR = ctypes.POINTER(CHAR)
LPTSTR = ctypes.c_char_p
BYTE = ctypes.c_ubyte
LPBYTE = ctypes.POINTER(BYTE)
BYREF = ctypes.byref
POINTER = ctypes.POINTER
MAX_PATH = 260
UINT_PTR = ctypes.c_ulong

SIZEOF = ctypes.sizeof

FALSE = 0
TRUE  = 1

if platform.architecture()[0] == "64bit":
    LONG = ctypes.c_longlong
    ULONG_PTR = ctypes.c_ulonglong
elif platform.architecture()[0] == "32bit":
    LONG = ctypes.c_long
    ULONG_PTR = ctypes.c_ulong
else:
    raise Exception("Not support plaotform: %s" % platform.architecture())

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("cntUsage", DWORD),
        ("th32ProcessID", DWORD),
        ("th32DefaultHeapID", ULONG_PTR), # 64bit or 32bit
        ("th32ModuleID", DWORD),
        ("cntThreads", DWORD),
        ("th32ParentProcessID", DWORD),
        ("pcPriClassBase", DWORD),
        ("dwFlags", DWORD),
        ("szExeFile", TCHAR * MAX_PATH),
    ]


class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('hProcess', HANDLE),
        ('hThread', HANDLE),
        ('dwProcessId', DWORD),
        ('dwThreadId', DWORD),
    ]


class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ('cb', DWORD),
        ('lpReserved', LPSTR),
        ('lpDesktop', LPSTR),
        ('lpTitle', LPSTR),
        ('dwX', DWORD),
        ('dwY', DWORD),
        ('dwXSize', DWORD),
        ('dwYSize', DWORD),
        ('dwXCountChars', DWORD),
        ('dwYCountChars', DWORD),
        ('dwFillAttribute', DWORD),
        ('dwFlags', DWORD),
        ('wShowWindow', WORD),
        ('cbReserved2', WORD),
        ('lpReserved2', LPBYTE),
        ('hStdInput', HANDLE),
        ('hStdOutput', HANDLE),
        ('hStdError', HANDLE),
    ]


class FLOATING_SAVE_AREA(ctypes.Structure):
    _fields_ = [
        ('ControlWord', DWORD),
        ('StatusWord', DWORD),
        ('TagWord', DWORD),
        ('ErrorOffset', DWORD),
        ('ErrorSelector', DWORD),
        ('DataOffset', DWORD),
        ('DataSelector', DWORD),
        ('RegisterArea', BYTE * 80),
        ('Cr0NpxState', DWORD),
    ]


class CONTEXT(ctypes.Structure):
    _fields_ = [
        ('ContextFlags', DWORD),
        ('Dr0', DWORD),
        ('Dr1', DWORD),
        ('Dr2', DWORD),
        ('Dr3', DWORD),
        ('Dr6', DWORD),
        ('Dr7', DWORD),
        ('FloatSave', FLOATING_SAVE_AREA),
        ('SegGs', DWORD),
        ('SegFs', DWORD),
        ('SegEs', DWORD),
        ('SegDs', DWORD),
        ('Edi', DWORD),
        ('Esi', DWORD),
        ('Ebx', DWORD),
        ('Edx', DWORD),
        ('Ecx', DWORD),
        ('Eax', DWORD),
        ('Ebp', DWORD),
        ('Eip', DWORD),
        ('SegCs', DWORD),
        ('EFlags', DWORD),
        ('Esp', DWORD),
        ('SegSs', DWORD),
        ('ExtendedRegisters', BYTE * 512),
    ]


class EXCEPTION_RECORD(ctypes.Structure):
    pass
EXCEPTION_RECORD._fields_ = [
        ('ExceptionCode', DWORD),
        ('ExceptionFlags', DWORD),
        ('ExceptionRecord', ctypes.POINTER(EXCEPTION_RECORD)),
        ('ExceptionAddress', PVOID),
        ('NumberParameters', DWORD),
        ('ExceptionInformation', UINT_PTR * 15),
    ]


class EXCEPTION_DEBUG_INFO(ctypes.Structure):
    _fields_ = [
        ('ExceptionRecord', EXCEPTION_RECORD),
        ('dwFirstChance', DWORD),
    ]

# macos compatability.
try:
    PTHREAD_START_ROUTINE = ctypes.WINFUNCTYPE(DWORD, ctypes.c_void_p)
except:
    PTHREAD_START_ROUTINE = ctypes.CFUNCTYPE(DWORD, ctypes.c_void_p)
LPTHREAD_START_ROUTINE = PTHREAD_START_ROUTINE
class CREATE_THREAD_DEBUG_INFO(ctypes.Structure):
    _fields_ = [
        ('hThread', HANDLE),
        ('lpThreadLocalBase', LPVOID),
        ('lpStartAddress', LPTHREAD_START_ROUTINE),
    ]

class CREATE_PROCESS_DEBUG_INFO(ctypes.Structure):
    _fields_ = [
        ('hFile', HANDLE),
        ('hProcess', HANDLE),
        ('hThread', HANDLE),
        ('lpBaseOfImage', LPVOID),
        ('dwDebugInfoFileOffset', DWORD),
        ('nDebugInfoSize', DWORD),
        ('lpThreadLocalBase', LPVOID),
        ('lpStartAddress', LPTHREAD_START_ROUTINE),
        ('lpImageName', LPVOID),
        ('fUnicode', WORD),
    ]

class EXIT_THREAD_DEBUG_INFO(ctypes.Structure):
    _fields_ = [
        ('dwExitCode', DWORD),
    ]

class EXIT_PROCESS_DEBUG_INFO(ctypes.Structure):
    _fields_ = [
        ('dwExitCode', DWORD),
    ]

class LOAD_DLL_DEBUG_INFO(ctypes.Structure):
    _fields_ = [
        ('hFile', HANDLE),
        ('lpBaseOfDll', LPVOID),
        ('dwDebugInfoFileOffset', DWORD),
        ('nDebugInfoSize', DWORD),
        ('lpImageName', LPVOID),
        ('fUnicode', WORD),
    ]

class UNLOAD_DLL_DEBUG_INFO(ctypes.Structure):
    _fields_ = [
        ('lpBaseOfDll', LPVOID),
    ]

class OUTPUT_DEBUG_STRING_INFO(ctypes.Structure):
    _fields_ = [
        ('lpDebugStringData', LPSTR),
        ('fUnicode', WORD),
        ('nDebugStringLength', WORD),
    ]

class RIP_INFO(ctypes.Structure):
    _fields_ = [
        ('dwError', DWORD),
        ('dwType', DWORD),
    ]

class DEBUG_EVENT_DOLLAR(ctypes.Structure):
    _fields_ = [
        ('Exception', EXCEPTION_DEBUG_INFO),
        ('CreateThread', CREATE_THREAD_DEBUG_INFO),
        ('CreateProcessInfo', CREATE_PROCESS_DEBUG_INFO),
        ('ExitThread', EXIT_THREAD_DEBUG_INFO),
        ('ExitProcess', EXIT_PROCESS_DEBUG_INFO),
        ('LoadDll', LOAD_DLL_DEBUG_INFO),
        ('UnloadDll', UNLOAD_DLL_DEBUG_INFO),
        ('DebugString', OUTPUT_DEBUG_STRING_INFO),
        ('RipInfo', RIP_INFO),
    ]
class DEBUG_EVENT(ctypes.Structure):
    _fields_ = [
        ('dwDebugEventCode', DWORD),
        ('dwProcessId', DWORD),
        ('dwThreadId', DWORD),
        ('u', DEBUG_EVENT_DOLLAR),
    ]

class LUID(ctypes.Structure):
    _fields_ = [
        ('LowPart', DWORD),
        ('HighPart', LONG),
    ]

class LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ('Luid', LUID),
        ('Attributes', DWORD),
    ]
class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [
        ('PrivilegeCount', DWORD),
        ('Privileges', LUID_AND_ATTRIBUTES * 1),
    ]

# macos compatability.
kernel32 = ctypes.windll.kernel32
advapi32 = ctypes.windll.advapi32

###
### manually declare various #define's as needed.
###

PROCESS_TERMINATE              = 0x00000001
TH32CS_SNAPPROCESS             = 0x00000002

INFINITE                       = 0xFFFFFFFF
INVALID_HANDLE_VALUE           = 0xFFFFFFFF

# debug event codes.
EXCEPTION_DEBUG_EVENT          = 0x00000001
CREATE_THREAD_DEBUG_EVENT      = 0x00000002
CREATE_PROCESS_DEBUG_EVENT     = 0x00000003
EXIT_THREAD_DEBUG_EVENT        = 0x00000004
EXIT_PROCESS_DEBUG_EVENT       = 0x00000005
LOAD_DLL_DEBUG_EVENT           = 0x00000006
UNLOAD_DLL_DEBUG_EVENT         = 0x00000007
OUTPUT_DEBUG_STRING_EVENT      = 0x00000008
RIP_EVENT                      = 0x00000009
USER_CALLBACK_DEBUG_EVENT      = 0xDEADBEEF     # added for callback support in debug event loop.

# debug exception codes.
EXCEPTION_ACCESS_VIOLATION     = 0xC0000005
EXCEPTION_BREAKPOINT           = 0x80000003
EXCEPTION_GUARD_PAGE           = 0x80000001
EXCEPTION_SINGLE_STEP          = 0x80000004

# hw breakpoint conditions
HW_ACCESS                      = 0x00000003
HW_EXECUTE                     = 0x00000000
HW_WRITE                       = 0x00000001

CONTEXT_CONTROL                = 0x00010001
CONTEXT_FULL                   = 0x00010007
CONTEXT_DEBUG_REGISTERS        = 0x00010010
CREATE_NEW_CONSOLE             = 0x00000010
DBG_CONTINUE                   = 0x00010002
DBG_EXCEPTION_NOT_HANDLED      = 0x80010001
DBG_EXCEPTION_HANDLED          = 0x00010001
DEBUG_PROCESS                  = 0x00000001
DEBUG_ONLY_THIS_PROCESS        = 0x00000002
EFLAGS_RF                      = 0x00010000
EFLAGS_TRAP                    = 0x00000100
ERROR_NO_MORE_FILES            = 0x00000012
FILE_MAP_READ                  = 0x00000004
FORMAT_MESSAGE_ALLOCATE_BUFFER = 0x00000100
FORMAT_MESSAGE_FROM_SYSTEM     = 0x00001000
INVALID_HANDLE_VALUE           = 0xFFFFFFFF
MEM_COMMIT                     = 0x00001000
MEM_DECOMMIT                   = 0x00004000
MEM_IMAGE                      = 0x01000000
MEM_RELEASE                    = 0x00008000
PAGE_NOACCESS                  = 0x00000001
PAGE_READONLY                  = 0x00000002
PAGE_READWRITE                 = 0x00000004
PAGE_WRITECOPY                 = 0x00000008
PAGE_EXECUTE                   = 0x00000010
PAGE_EXECUTE_READ              = 0x00000020
PAGE_EXECUTE_READWRITE         = 0x00000040
PAGE_EXECUTE_WRITECOPY         = 0x00000080
PAGE_GUARD                     = 0x00000100
PAGE_NOCACHE                   = 0x00000200
PAGE_WRITECOMBINE              = 0x00000400
PROCESS_ALL_ACCESS             = 0x001F0FFF
SE_PRIVILEGE_ENABLED           = 0x00000002
SW_SHOW                        = 0x00000005
THREAD_ALL_ACCESS              = 0x001F03FF
TOKEN_ADJUST_PRIVILEGES        = 0x00000020
UDP_TABLE_OWNER_PID            = 0x00000001
VIRTUAL_MEM                    = 0x00003000

# for NtSystemDebugControl()
SysDbgReadMsr                  = 16
SysDbgWriteMsr                 = 17

# for mapping TCP ports and PIDs
AF_INET                        = 0x00000002
AF_INET6                       = 0x00000017
MIB_TCP_STATE_LISTEN           = 0x00000002
TCP_TABLE_OWNER_PID_ALL        = 0x00000005
