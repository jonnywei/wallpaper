#!/usr/bin/python
# -*- coding: utf-8 -*-

#得到屏幕的分辨率
from gi.repository import Gtk
def getScreenResolution():
    display = Gtk.Window().get_display()
    screen = display.get_default_screen()
    width = screen.get_width ()
    height = screen.get_height()
    return width ,height

    
