"""Defining types and setting function prototypes for ftd2xx.dll"""

from ctypes import *

libftdi = WinDLL('ftd2xx', use_last_error=True)

#type aliases
DWORD       = c_ulong
ULONG       = c_ulong
WORD        = c_ushort

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

#useless :-/
class FTDCB(Structure):
    _fields_ = [
		("DCBlength", DWORD),
		("BaudRate", DWORD),
		("fBinary", DWORD, 1),
		("fParity", DWORD, 1),
		("fOutxCtsFlow", DWORD, 1),
		("fOutxDsrFlow", DWORD, 1),
		("fDtrControl", DWORD, 2),
		("fDsrSensitivity", DWORD, 1),
		("fTXContinueOnXoff", DWORD, 1),
		("fOutX", DWORD, 1),
		("fInX", DWORD, 1),
		("fErrorChar", DWORD, 1),
		("fNull", DWORD, 1),
		("fRtsControl", DWORD, 2),
		("fAbortOnError", DWORD, 1),
		("fDummy2", DWORD, 17),
		("wReserved", WORD),
		("XonLim", WORD),
		("XoffLim", WORD),
		("ByteSize", c_char),
		("Parity", c_char),
		("StopBits", c_char),
		("XonChar", c_char),
		("XoffChar", c_char),
		("ErrorChar", c_char),
		("EofChar", c_char),
		("EvtChar", c_char),
		("wReserved1", WORD)
    ]

#prototypes:
libftdi.FT_Close.argtypes = [FT_HANDLE]

libftdi.FT_CreateDeviceInfoList.argtypes = [POINTER(DWORD)]
libftdi.FT_CreateDeviceInfoList.restype = ULONG

libftdi.FT_GetDeviceInfoList.argtypes = [POINTER(FT_DEVICE_LIST_INFO_NODE), POINTER(DWORD)]
libftdi.FT_GetDeviceInfoList.restype = ULONG

libftdi.FT_GetLibraryVersion.argtypes = [POINTER(DWORD)]
libftdi.FT_GetLibraryVersion.restype = ULONG

libftdi.FT_GetQueueStatus.argtypes = [FT_HANDLE, POINTER(DWORD)]
libftdi.FT_GetQueueStatus.restype = ULONG

libftdi.FT_OpenEx.argtypes = [c_void_p, DWORD, POINTER(FT_HANDLE)]
libftdi.FT_OpenEx.restype = ULONG

libftdi.FT_Read.argtypes = [FT_HANDLE, c_void_p, DWORD, POINTER(DWORD)]
libftdi.FT_Read.restype = ULONG

libftdi.FT_SetBaudRate.argtypes = [FT_HANDLE, DWORD]
libftdi.FT_SetBaudRate.restype = ULONG

libftdi.FT_SetDataCharacteristics.argtypes = [FT_HANDLE, c_char, c_char, c_char]

libftdi.FT_Write.argtypes = [FT_HANDLE, c_void_p, DWORD, POINTER(DWORD)]
libftdi.FT_Write.restype = ULONG

libftdi.FT_W32_GetCommState.argtypes = [FT_HANDLE, POINTER(FTDCB)]