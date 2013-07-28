#!/usr/bin/python

from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Gio, GObject,Notify

class ImageEventBox(Gtk.EventBox):
    
    def __init__(self):
        super(ImageEventBox,self).__init__()



GObject.type_register(ImageEventBox)
#GObject.signal_new('image-load-complete', ImageEventBox, GObject.SIGNAL_RUN_FIRST | GObject.SIGNAL_ACTION,
#                   GObject.TYPE_NONE, (GObject.TYPE_STRING, ))
GObject.signal_new('image-load-init', ImageEventBox, GObject.SIGNAL_RUN_FIRST | GObject.SIGNAL_ACTION,
                    GObject.TYPE_NONE, (GObject.TYPE_STRING, GObject.TYPE_OBJECT,GObject.TYPE_STRING, ))

        
        
