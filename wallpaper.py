#!/usr/bin/python
# -*- coding: utf-8 -*-


#

from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Gio, GObject

from os import path

class WallpaperApp:

    def __init__(self):

        self.window = Gtk.Window(title= '搜狗壁纸')
        self.window.connect('delete-event',Gtk.main_quit)
        self.window.set_border_width(8)

        self.grid = Gtk.Grid( )
        self.grid.set_border_width(8)

        self.window.add(self.grid)

        frame = Gtk.Frame()
        #align = Gtk.Alignment(xalign=0.5, 
        #                      yalign=0.5, 
         #                     xscale=0, 
        #                      yscale=0)
        #align.add(frame)
        #self.grid.pack_start(align, False, False, 0)

        self.base_path = '/home/wjj/.wallpaper/wallpaper/'
        if not path.isdir(self.base_path):
            self.base_path = path.join('', self.base_path)
   
        #self.addImage('22.jpg')
        #
        #self.addImage('2.gif')
        #self.addImage('22.jpeg')
        i = 0
        left = 0
        top  = 0
        for file in list_wallpaper_file():
            
            left = (i) /6 
            top  = (i) % 6
            print left , top
            self.addImage(file, top, left, 1, 1)
            i =  i+1
            if i > 35:
                break
        self.window.show_all()
    def addImage(self,img_name, left, top, width ,height):
        frame = Gtk.Frame()
        try:
            img_path = path.join(self.base_path, img_name)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(img_path)
        except GObject.GError as e:
            dialog = Gtk.MessageDialog(self.window,
                                       Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                       Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.CLOSE,
                                       e.message)
 
            dialog.show()
            dialog.connect('response', lambda x,y: dialog.destroy())

        image = Gtk.Image.new_from_pixbuf(pixbuf)
        frame.add(image)
        #self.grid.add(frame)
        self.grid.attach(frame,left, top, width ,height)

if __name__ =='__main__':
    app = WallpaperApp()
    Gtk.main()
    
        

        
