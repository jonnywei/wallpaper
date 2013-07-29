#!/usr/bin/python
# -*- coding: utf-8 -*-


#

from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Gio, GObject,Notify
from gi.repository import AppIndicator3 as AppIndicator
from os import path
from multiprocessing.pool import ThreadPool
import os
import threading
import sys
import Queue
import logging

from sogou import SouGou
import util
import screen
import changeWallpaper
import image_event_box  
import random



sougou = SouGou()

large_img_save_dir = None

class WallpaperApp:

    def __init__(self):

        if not Notify.init("WallpaperApp"):
            raise ImportError("Couldn't initialize libnotify")
        
        self.window = Gtk.Window(title= '搜狗壁纸')
        
        self.scroll_window = Gtk.ScrolledWindow()
        self.scroll_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        #
        self.window.connect('delete-event',self.hidden_window)
        self.window.set_border_width(8)
        self.window.set_size_request(1024,768)
        
        
        self.grid = Gtk.Grid( )
        self.grid.set_border_width(8)
        self.scroll_window.add_with_viewport(self.grid)

        self.window.add(self.scroll_window)
        #self.window.add(self.grid)

        self.base_path = '/home/wjj/.wallpaper/wallpaper/'
        if not path.isdir(self.base_path):
            self.base_path = path.join('', self.base_path)

        self.queue = Queue.Queue()

        self.show_wallpaper_page_size = 10
        
        self.wallpaper_file_list = sougou.getImgList()
        self.current_image_count = 0

        self.executor = ThreadPool(processes = 20)
        
        #ltit = LoadThumbImageThread(self,  self.wallpaper_file_list, self.current_image_count)
        #ltit.run()

        self.init_download_thumb_image()
        self.dynamic_show_wallpaper()
        #i = 0
        #left = 0
        #top  = 0
        #for file in self.wallpaper_file_list:
            
            #left = (i) /5 
            #top  = (i) % 5
            #print left , top
            
            #self.addImage(file, top, left, 1, 1)
            #i =  i+1
            #if i >self.show_wallpaper_page_size-10:
            ##    break

        #
        

        
        
        #GObject.timeout_add(1000, self.dynamic_show_wallpaper)
        #self.window.show_all()
    
    def init_download_thumb_image(self):
        print "init_download_thumb_image"
        i = 0
        rand =random.Random()
        total = len(self.wallpaper_file_list)
        start = int (rand.random() * total)
        if start + self.show_wallpaper_page_size > total:
            start = total - self.show_wallpaper_page_size
        new_wallpaper_file_list =  self.wallpaper_file_list[ start:]
        for file in new_wallpaper_file_list:
            #self.executor.apply_async( self.download_thumb_image, (file,) )
            self.download_thumb_image(file)
            i =  i+1
            if i >= self.show_wallpaper_page_size:
                break
        

    
    #动态的展示
    def dynamic_show_wallpaper(self):
        items =[]
        while 1:
            try:
                items.append(self.queue.get_nowait())
            except Queue.Empty, e:
                break
        for img_path in  items:
            
            #img_path = '/home/wjj/.wallpaper/wallpaper/330534_s_90_2.webp.png'
            image = Gtk.Image()
            image.set_from_file(img_path)
            image.show()
            #self.addImage('/home/wjj/.wallpaper/wallpaper/10091_s_90_2.webp.png', 100, 100, 1, 1)
            #self.frame.show()
            eventbox = Gtk.EventBox()
            eventbox.add(image)
            eventbox.connect('button-press-event', self.on_image_clicked, img_path)
            self.frame = Gtk.Frame()
            self.frame.add(eventbox)
           
            left = (self.current_image_count) /5 
            top  = (self.current_image_count) % 5
            print left , top
            
            self.grid.attach(self.frame, top, left,1,1)
            self.current_image_count = self.current_image_count + 1
            
            self.window.show_all()
        
        

    def get_wallpaper_file_list(self):
        img_list =  sougou.getImgList()
        for img in img_list:
            print img
        return img_list

    def download_thumb_image(self ,image_name ):
        try:
            print 'download_thumb_image ',image_name 
            img_path = sougou.downloadImageAndSave( image_name)
            self.queue.put(img_path)
            #img_path = path.join(self.base_path, self.image_name)
            #print 'img_path', img_path
            #pixbuf = GdkPixbuf.Pixbuf.new_from_file(img_path)
        except GObject.GError as e:
            print 'error download image'

        
                         
    def addImage(self,img_name, left, top, width ,height):
        self.frame = Gtk.Frame()
        self.frame.set_border_width(8) #间隔大小
        #self.eb = Gtk.EventBox()
        self.eb = image_event_box.ImageEventBox()
        #self.eb.add(image)
        self.frame.add(self.eb)
        #progressbar = Gtk.ProgressBar()
        #self.frame.add(progressbar)
        #button = Gtk.CheckButton("Show text")
        #self.frame.add(button)
        #self.eb.connect('button-press-event', self.on_image_clicked, img_path)
        #self.grid.add(frame)
        self.grid.attach(self.frame,left, top, width ,height)

    def on_image_clicked(self, widget, event,img_path):
        #image = Gtk.Image()
        #image.set_from_file('/home/wjj/.wallpaper/wallpaper/339575_s_90_2.webp.png')
        #image.show()
        #eventbox = Gtk.EventBox()
        #eventbox.add(image)
        #eventbox.connect('button-press-event', self.on_image_clicked, img_path)
        #frame = Gtk.Frame()
        #frame.add(eventbox)
       
        #self.grid.attach(frame,3, 0, 1, 1)
        #self.window.show_all()
        
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

    def on_image_load_complete(self, widget, event):
        print 'on_image_load_complete'

    def on_image_load_init(self, widget, event, eventbox, image_name):
        print 'on_image_load_init execute'
        
        try:
            print 'DOWNLOAD', image_name 
            img_path = sougou.downloadImageAndSave( image_name)
            #img_path = path.join(self.base_path, self.image_name)
            print 'img_path', img_path
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(img_path)
        except GObject.GError as e:
            dialog = Gtk.MessageDialog(None,
                                       Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                       Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.CLOSE,
                                       e.message)
 
            dialog.show()
            dialog.connect('response', lambda x,y: dialog.destroy())

        image = Gtk.Image.new_from_pixbuf(pixbuf)
        eventbox.add(image)
        eventbox.connect('button-press-event', self.on_image_clicked, img_path) 
       
        
        
    def about(self,widget):
        self.about_dialog = Gtk.AboutDialog()
        self.about_dialog.set_program_name('搜狗壁纸')
        self.about_dialog.set_version('0.1')
        self.about_dialog.connect('response',self.about_close)
        self.about_dialog.show()
        
    def about_close(self, widget, event=None):
        """ Menu callback to close About dialog """
        #log.debug("Indicator: closing About dialog")
        self.about_dialog.destroy()

    def hidden_window(self,widget,event=None):
        self.window.hide()
    def show_window(self, event):
        self.__init__()
        self.window.show_all()
    def quit_program(self,event):
        Gtk.main_quit()
     
class LoadThumbImageThread(threading.Thread):
    def __init__(self,app,wallpaper_file_list,current_image_count):
        #super(LoadThumbImageThread, self).__init__()
        threading.Thread.__init__(self)
        self.wallpaper_file_list = wallpaper_file_list
        self.current_image_count = current_image_count
        self.app = app
        self.executor = app.executor


    def download_thumb_image(self ,image_name ):
        try:
            print 'download_thumb_image ',image_name 
            img_path = sougou.downloadImageAndSave( image_name)
            self.app.queue.put(img_path)
            #img_path = path.join(self.base_path, self.image_name)
            #print 'img_path', img_path
            #pixbuf = GdkPixbuf.Pixbuf.new_from_file(img_path)
        except GObject.GError as e:
            print 'error download image'

    def run(self):
        print "thread run"
        self.executor = ThreadPool(processes = 5)
        i = 0
        for file in self.wallpaper_file_list:
            self.executor.apply_async( self.download_thumb_image, (file,) )
            
            #dhpt = DownloadThumbWallpaperThread(file)
            #dhpt.start()
            i =  i+1
            if i > self.app.show_wallpaper_page_size:
                break

        
    def run2(self):
        self.frame = Gtk.Frame()
        self.frame.set_border_width(8) #间隔大小
        
        #self.eb = Gtk.EventBox()
        self.app.eb = self.eb = image_event_box.ImageEventBox()
        
        progressbar = Gtk.ProgressBar()
        self.frame.add(self.eb)
        self.frame.add(progressbar)

        button = Gtk.CheckButton("Show text")

        self.frame.add(button)
        
        
        self.eb.connect('image-load-init',self.app.on_image_load_init)
        

        #trigger load init
        #self.eb.emit('image-load-init','pressed',self.eb, self.image_name)
           
        #self.grid.add(frame)
        self.grid.attach(self.frame,self.left, self.top, 1 ,1)
        #self.app.window.show_all()
        print "Load OK"
        
class DownloadThumbWallpaperThread(threading.Thread):
    def __init__(self,image_name):
        threading.Thread.__init__(self)
        self.image_name= image_name
        

    def run(self):
        try:
            print 'DOWNLOAD', self.image_name 
            img_path = sougou.downloadImageAndSave(self.image_name)
            #img_path = path.join(self.base_path, self.image_name)
            print 'img_path', img_path
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(img_path)
        except GObject.GError as e:
            dialog = Gtk.MessageDialog(None,
                                       Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                       Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.CLOSE,
                                       e.message)
 
            dialog.show()
            dialog.connect('response', lambda x,y: dialog.destroy())

        image = Gtk.Image.new_from_pixbuf(pixbuf)
        

        

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
    # init GLib/GObject
    GObject.threads_init()
    #GLib.threads_init()

    # init Gdk threads and get Gdk lock
    #Gdk.threads_init()
    #Gdk.threads_enter()

    # init Gtk
    Gtk.init(None)

    app = WallpaperApp()
    
    ind = AppIndicator.Indicator.new (
                        "example-simple-client",
                        "indicator-messages",
                        AppIndicator.IndicatorCategory.APPLICATION_STATUS)
    ind.set_status (AppIndicator.IndicatorStatus.ACTIVE)
    ind.set_attention_icon ("indicator-messages-new")
    ind.set_icon('/usr/share/indicator-weather/media/icon.png')

  # create a menu
    menu = Gtk.Menu()
    menu_item_show_window = Gtk.MenuItem('显示...')
    menu_item_show_window.connect('activate',app.show_window)
    menu_item_show_window.show()
    menu.append(menu_item_show_window)
    
    menu_item_about_show = Gtk.MenuItem('关于搜狗壁纸')
    menu_item_about_show.connect('activate',app.about)
    menu_item_about_show.show()
    menu.append(menu_item_about_show)
    
    menu_item_quit = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_QUIT,None)
    menu_item_quit.connect('activate', app.quit_program)
    menu_item_quit.show()
    menu.append(menu_item_quit)

    ind.set_menu(menu)
    Gtk.main()

        # release Gdk lock
    Gdk.threads_leave()
    
    
        

        
