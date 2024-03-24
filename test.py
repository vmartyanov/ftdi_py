"""Sample program to show how it works."""

import time

import ftdi

def main() -> None:
    """Main function."""
    dev = ftdi.get_devices()[0]

    print (f"Working with {dev.description}, S/N {dev.ser_number}")

    with dev.open():
        while True:
            dev.serial_write(b"\x00" * 16)
            time.sleep(0.5)




if __name__ == "__main__":
    main()
