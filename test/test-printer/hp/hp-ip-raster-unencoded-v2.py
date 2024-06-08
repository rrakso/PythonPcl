#!/usr/bin/env python
# -*- coding: utf8 -*-
"""hp-ip-raster-unencoded-v2.py

How to print a Raster Graphic on NETWORKED HP Printer.
This sample use no compression method.

*** THIS EXAMPLE USE RASTER METHOD DEFINED ON THE HpPclDocument ***

This method can allow you to easily improve the design of document
content BUT required the usage of the PCL Symbol Set "PC-850 multilingual" 
sheet.  
  
Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  27 feb 2015 - Dominique - v 0.1 (created from hp-ip-raster-unencoded.py with better coding)
"""
from pypcl import *
from pypcl import HpPclDocument

PRINTER_IP = '192.168.1.206'
PRINTER_PORT = 9100
PRINTER_ENCODING = 'cp850'


def print_raster_graphic_unencoded(printer_socket):
    """ Generate the PCL document containg a raw graphic image.
        This sample is a basic implementation injecting raw esc sequences

    parameters:
            printer_socket : tuple (PRINTER_IP, PRINTER_PORT). On which
                                             socket to print.
    """

    print('Minimal Raster Graphic printing')
    print('-------------------------------')
    print('Printer IP: %s\nPrinter Port: %i' % printer_socket)
    medium = PrinterSocketAdapter(printer_socket)

    # Very simple printout + usual initialization commands
    d = HpPclDocument('cp850', medium)
    d.reset_printer()  # PCL to reset the printer

    d.write(u'Raster Graphic Test')
# Move the cursor to PCL unit position (300,400) within the PCL
# coordinate system
#   x-position: 300 unit @ 300 dot/inch --> 1 inch --> 2.54cm
#   y-position: 400 unit @ 300 dot/inch --> 1.33 inch --> 3.38cm
    d.cursor_move((300, 400))

    # Set the Raster Graphics resolution (75 dpi)
    d.raster_set_resolution()

    # Raster Graphic Presentation Mode
    # -> Orientation of the logical page
    d.raster_presentation_mode()

    # Start Raster Graphic
    #  0 -> At x-position = 0
    #  1 -> At current x-position of the cursor position
    d.raster_start_graphic(at_current_cursor_pos=True)

    # sending 5 rows of datas
    #   Source: "PCL 5 Printer Langage Technical Reference.pdf", page 339
    # Raster Image Data                       Command Data
    # Dot
    # Row byte 1   byte 2   byte 3   byte 4     Decimal Equivalent
    # 1   00000000 00000000 10000000 00000000   <esc>*b4W[0, 0,128, 0]
    # 2   00000000 00000000 11000000 00000000   <esc>*b4W[0, 0,192, 0]
    # 3   00000000 00000000 11100000 00000000   <esc>*b4W[0, 0,224, 0]
    # 4   00000000 00000000 11110000 00000000   <esc>*b4W[0, 0,240, 0]
    # 5   00000000 00000000 11111000 00000000   <esc>*b4W[0, 0,248, 0]

    # Print the image, stored as list of bit (encoded into string for
    # easy code writing, use a space every 8 bits for reading,
    # the code space are ignored)
    d.raster_senddata_str(['00000000 00000000 10000000 00000000',
                           '01100110 00000000 11000000 00000000',
                           '00100010 01000000 11100000 00000000',
                           '10000000 10000000 11110000 00000000',
                           '01111111 00000000 11111000 0000000'])

    # End Raster Graphic
    d.raster_end_graphic()

    # Move to position
# Move the cursor to PCL unit position (300,400) within the PCL
# coordinate system
#    This example use the 300 dots/inch as refernce for coordonate
#    y-pos = under the raster --> 4 cm --> 1.57 inch @ 300 dot/inch --> 472 dots
    d.cursor_move((300, 472))

    d.writeln(u'End of test')

    medium.open()  # Open the media for transmission
    try:
        d.send()  # Send the content of the current document
    finally:
        medium.close()

    del (d)
    del (medium)


if __name__ == '__main__':
    print_raster_graphic_unencoded((PRINTER_IP, PRINTER_PORT))
