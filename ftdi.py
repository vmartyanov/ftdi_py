"""Python wrapper for ftd2xx.dll"""

from ctypes import *
from types import TracebackType

from defines import *

#check library version
LIB_VERSION = DWORD()
__status = libftdi.FT_GetLibraryVersion(byref(LIB_VERSION))
if __status:
    raise RuntimeError(f"Error getting FTDI library version! {__status}")

if LIB_VERSION.value != 0x30216:
    raise RuntimeError("Unsupported ftd2xx.dll version!")

DEV_TYPES = {0: "232BM",
             1: "232AM",
             2: "100AX",
             3: "UNKNOWN",
             4: "2232C",
             5: "232R",
             6: "2232H",
             7: "4232H",
             8: "232H",
             9: "X_SERIES",
            }

class FtdiDev():
    """Class, representing FTDI-device."""
    def __init__(self, info_node: FT_DEVICE_LIST_INFO_NODE):
        """Init the device."""
        #todo maybe we need a right fields definition to avoid decode()?
        self.description = info_node.Description.decode()
        self.ser_number = info_node.SerialNumber.decode()
        self.type_int = info_node.Type
        self.type_str = DEV_TYPES[self.type_int]

        self.handle = FT_HANDLE(0)

    def __enter__(self) -> None:
        """Context manager enter."""
        handle = FT_HANDLE()
        status = libftdi.FT_OpenEx(self.ser_number.encode("ascii"), 0x01, byref(handle))
        if status:
            print (f"Error opening device {status}")
        self.handle = handle

    def __exit__(self,
                 exc_type: type[BaseException] | None,
                 exc_val: BaseException | None,
                 exc_tb: TracebackType | None) -> None:
        """Context manager exit."""
        if self.handle:
            libftdi.FT_Close(self.handle)
        self.handle = FT_HANDLE(0)

    def open(self) -> "FtdiDev":
        """Thunk to have with dev.open()."""
        return self

    def serial_write(self, data: bytes) -> None:
        """Write to COM-port."""
        #todo return number of bytes written?
        if not self.handle:
            raise ValueError ("Invalid handle")

        written = DWORD(0)
        libftdi.FT_Write(self.handle, data, len(data), byref(written))

    def serial_read(self, count: int) -> None | bytes:
        """Read from COM-port."""
        if not self.handle:
            raise ValueError ("Invalid handle")

        read = DWORD(0)
        buffer = create_string_buffer(count)
        libftdi.FT_Read(self.handle, buffer, count, byref(read))
        return buffer.raw

    def set_baud_rate(self, baud_rate: int) -> None:
        """Set baud rate"""
        if not self.handle:
            raise ValueError ("Invalid handle")

        speed = DWORD(baud_rate)
        status = libftdi.FT_SetBaudRate(self.handle, speed)
        if status:
            raise RuntimeError(f"Error setting baudrate {status}")

    def set_chars(self, data_bits: int, parity: int, stop_bits: int) -> None:
        """Set data len, parity and stop bits."""
        if not self.handle:
            raise ValueError ("Invalid handle")

        status = libftdi.FT_SetDataCharacteristics(self.handle, c_char(data_bits), c_char(stop_bits), c_char(parity))
        if status:
            raise RuntimeError(f"Error setting data characteristics {status}")


def get_devices() -> list[FtdiDev]:
    """Get a list of available FTDI devices."""
    ret: list[FtdiDev] = []

    count = DWORD(0)
    num_devs = DWORD(0)

    status = libftdi.FT_CreateDeviceInfoList(byref(count))
    if status:
        print (f"Error calling FT_CreateDeviceInfoList: {status:x}")
        return ret

    info_list = (FT_DEVICE_LIST_INFO_NODE * count.value)()
    status = libftdi.FT_GetDeviceInfoList(info_list, byref(num_devs))
    if status:
        print (f"Error calling FT_GetDeviceInfoList: {status:x}")
        return ret

    if num_devs.value != count.value:
        print (f"WTF?! different devices count {count.value} != {num_devs.value}")

    for i in range(num_devs.value):
        ret.append(FtdiDev(info_list[i]))
    return ret
