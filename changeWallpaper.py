#!/usr/bin/python

from gi.repository import Gio

def changeWallpaper(file_name):
    SCHEMA = 'org.gnome.desktop.background'
    KEY    = 'picture-uri'
    gsettings = Gio.Settings.new(SCHEMA)
    gsettings.set_string(KEY,"file://"+file_name)

