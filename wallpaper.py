#!/usr/bin/python
# -*- coding: utf-8 -*-


#

from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Gio, GObject,Notify
from os import path
import os
import threading

from sogou import SouGou

import util
import screen
import changeWallpaper

sougou = SouGou()

large_img_save_dir = None


class WallpaperApp:

    def __init__(self):

        GLib.threads_init()

        if not Notify.init("WallpaperApp"):
            raise ImportError("Couldn't initialize libnotify")
  
         
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
        for file in util.list_wallpaper_file():
            
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
        eb = Gtk.EventBox()
        eb.add(image)
        progressbar = Gtk.ProgressBar()
        frame.add(eb)
        frame.add(progressbar)

        button = Gtk.CheckButton("Show text")
        frame.add(button)
        
        eb.connect('button-press-event', self.on_image_clicked, img_path)
        #self.grid.add(frame)
        self.grid.attach(frame,left, top, width ,height)

    def on_image_clicked(self, widget, event,img_path):
          
        print 'clicked'
         
        choose_img_dialog = ChooseImgDialog(self.window,img_path)
        #choose_img_dialog.action_area.remove(Gtk.STOCK_CANCEL)
     
        response = choose_img_dialog.run()

        
        
        #choose_img_dialog.
        if response == Gtk.ResponseType.OK:
            cwthread =  ChangeWallpaperThread(choose_img_dialog.large_img_id )
            cwthread.start()
            #changeWallpaper('/home/wjj/.wallpaper/wallpaper/large/350998')
            #success_notification = Notify.Notification.new ("搜狗壁纸","正在为您下载壁纸...","dialog-information")
            #success_notification.set_hint("transient", GLib.Variant.new_boolean(True))   #Gnome3 transient
            #success_notification.set_urgency(Notify.Urgency.NORMAL)
            #success_notification.set_timeout(3000)
            
            #success_notification.show () 
        elif response == Gtk.ResponseType.CANCEL:
            
            
            
            print "The Cancel button was clicked"

        choose_img_dialog.destroy()
       
     

class ChangeWallpaperThread(threading.Thread):
    def __init__(self,large_img_id):
        threading.Thread.__init__(self)
        self._large_img_id = large_img_id

    def run(self):
        scr = screen.getScreenResolution()
        large_img_save_dir = sougou.downloadLargeImg(self._large_img_id , scr[0] ,scr[1])
        changeWallpaper.changeWallpaper(large_img_save_dir)

        success_notification = Notify.Notification.new ("搜狗壁纸","您的壁纸已经设置成功!","/home/wjj/success.png")
        success_notification.set_hint("transient", GLib.Variant.new_boolean(True))   #Gnome3 transient
        success_notification.set_urgency(Notify.Urgency.NORMAL)
        success_notification.set_timeout(3000)
            
        success_notification.show () 
        print "Change Wallpaper OK"
        
#dialog box

class ChooseImgDialog(Gtk.Dialog):
    def __init__(self, parent,img_path):
        Gtk.Dialog.__init__(self, "设置壁纸", parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK ,Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        self.set_default_size(400, 400)
        
        
        img_name = os.path.basename(img_path)
        img_id = img_name.split('_')[0]
        self.large_img_id = img_id
       
        #print large_img_save_dir
        self.img_path = img_path
        box = self.get_content_area()
        try:
           
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.img_path,800,600,True)
            #pixbuf.scale_simple(200, 200,1)
        except GObject.GError as e:
            dialog = Gtk.MessageDialog(self.window,
                                       Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                       Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.CLOSE,
                                       e.message)
 
            dialog.show()
            dialog.connect('response', lambda x,y: dialog.destroy())

        image = Gtk.Image.new_from_pixbuf(pixbuf)
        
        box.add(image)

        #self.connect('size_allocate' ,self.resize_event)
        self.show_all()

    def resize_event(self, wiget ,event):
        
        
        box = self.get_content_area()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.img_path,self.get_allocated_width(),self.get_allocated_height(),True)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        box.clear()
        box.add(image)



if __name__ =='__main__':
    app = WallpaperApp()
    Gtk.main()
    
        

        
