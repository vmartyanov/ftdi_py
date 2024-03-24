"""Defining types and setting function prototypes for ftd2xx.dll"""

from ctypes import *

libftdi = WinDLL('ftd2xx', use_last_error=True)

#type aliases
DWORD       = c_ulong
ULONG       = c_ulong

FT_HANDLE   = c_void_p

#ftdi types
class FT_DEVICE_LIST_INFO_NODE(Structure):
    _fields_ = [
		("Flags", ULONG),
		("Type", ULONG),
		("ID", ULONG),
		("LocId", DWORD),
		("SerialNumber", c_char * 16),
		("Description", c_char * 64),
		("ftHandle", FT_HANDLE)
	]


#prototypes:
libftdi.FT_Close.argtypes = [FT_HANDLE]

libftdi.FT_CreateDeviceInfoList.argtypes = [POINTER(DWORD)]
libftdi.FT_CreateDeviceInfoList.restype = ULONG

libftdi.FT_GetDeviceInfoList.argtypes = [POINTER(FT_DEVICE_LIST_INFO_NODE), POINTER(DWORD)]
libftdi.FT_GetDeviceInfoList.restype = ULONG

libftdi.FT_GetLibraryVersion.argtypes = [POINTER(DWORD)]
libftdi.FT_GetLibraryVersion.restype = ULONG

libftdi.FT_OpenEx.argtypes = [c_void_p, DWORD, POINTER(FT_HANDLE)]
libftdi.FT_OpenEx.restype = ULONG

libftdi.FT_Read.argtypes = [FT_HANDLE, c_void_p, DWORD, POINTER(DWORD)]
libftdi.FT_Read.restype = ULONG

libftdi.FT_Write.argtypes = [FT_HANDLE, c_void_p, DWORD, POINTER(DWORD)]
libftdi.FT_Write.restype = ULONG
