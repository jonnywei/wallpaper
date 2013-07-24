#!/usr/bin/python
# -*- coding: utf-8 -*-

#适用工具类
import gzip
import os
dwebp = "dwebp"
home_dir = os.path.expanduser ('~')


def readGzip(file_name):
    f = gzip.open(file_name, 'rb')
    file_content = f.read()
    f.close()
    return file_content


#建立目录
def make_dir(dir_path):
    new_dir  = home_dir + '/' + dir_path
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
        return True
    return False

def get_absoulte_dir(dir_path):
    new_dir  = home_dir + '/' + dir_path
    return new_dir



def convert_webp_to_png(file_path,new_file_path):
    if new_file_path == None:
        new_file = file_path + ".png"
    cmd = "%s %s -o %s" % (dwebp,file_path, new_file_path)
    
    os.system(cmd)

def list_wallpaper_file():
    wallpaper_dir = home_dir +"/.wallpaper/wallpaper/"
    png_list = [file for file in os.listdir(wallpaper_dir) if file.endswith('.png')]
    return png_list
    
    
    
