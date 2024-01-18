#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 7.6
#  in conjunction with Tcl version 8.6
#    Nov 14, 2023 06:30:11 PM CET  platform: Windows NT
#    Nov 14, 2023 06:31:55 PM CET  platform: Windows NT

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import poehelper

_debug = True # False to eliminate debug printing from callback functions.

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    # _w1 = poehelper.PoE_Helper(_top1)
    _w1 = poehelper.gui(_top1)
    root.mainloop()

def pause_bot_command(*args):
    if _debug:
        print('poehelper_support.pause_bot_command')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def start_bot_command(*args):
    if _debug:
        print('poehelper_support.start_bot_command')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def stop_bot_command(*args):
    if _debug:
        print('poehelper_support.stop_bot_command')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

if __name__ == '__main__':
    poehelper.start_up()




