#!/usr/bin/env python
# -*- coding: utf8 -*-
"""zebra-usb-minimal.py

Test the minimal document printing on a USB Zebra TLP 2824 Plus printer
*** WHEN CUPS IS NOT INSTALLED!!! ***. 
  
if you are using a Zebra USB printer on a Linux Machine, you should
have a look to zebra-cups-minimal.py

Before starting this script, you should have a look to the demo-x.x files
where you will learn lots of things.

Copyright 2024 Oskar Jaskólski <oskarrro90@gmail.com>

Licence: CC-BY-SA-NC 
"""
from pypcl import *
from pypcl import ZplDocument
from pypcl import PrinterUsbAdapter

# These connection details are specified for the Zebra TLP 2824 Plus printer.
# To find out yours execute: `lsusb` and look for value of "ID".
# Sample command output: `Bus 001 Device 004: ID 0a5f:00a1 Zebra ZTC TLP 2824 Plus`
PRINTER_ID_VENDOR = 0x0a5f
PRINTER_ID_PRODUCT = 0x00a1

PRINTER_ENCODING = 'cp850'


def print_minimal_doc(idVendor, idProduct, encoding):
    """ Generate the mininal ZPL document and print it on USB-Serial printer.

    parameters:
            printer_serial : tuple (PRINTER_SERIAL, PRINTER_BAUD). On which
                                             serial port to print.
    """

    print('Minimal ZPL Document printing')
    print('-----------------------------')
    print(f'Printer USB: idVendor={idVendor}, idProduct={idProduct}')
    medium = PrinterUsbAdapter(idVendor, idProduct)

    # Very simple printout + usual initialization commands
    d = ZplDocument(encoding, medium)

    # Start a Print format
    d.format_start()

    # Write a BarCode field
    d.field(origin=(120, 11), font=d.font('E'), data=u'Hello')
    d.field(origin=(120, 42), font=d.font('E'), data=u'Wolrd!')
    d.field(origin=(100, 160), font=d.font('C'), data=u'Label print demo')
    d.field(origin=(70, 180), font=d.font(
        'C'), data=u'Using PythonPCL package')

    # End Print format
    d.format_end()

    medium.open()  # Open the media for transmission
    try:
        d.send()  # Send the content of the current document
    finally:
        medium.close()

    del d
    del medium


if __name__ == '__main__':
    print_minimal_doc(PRINTER_ID_VENDOR, PRINTER_ID_PRODUCT, PRINTER_ENCODING)
