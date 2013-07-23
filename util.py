#!/usr/bin/python
# -*- coding: utf-8 -*-

#适用工具类
import gzip
import os
def readGzip(file_name):
    f = gzip.open(file_name, 'rb')
    file_content = f.read()
    f.close()
    return file_content


#建立目录
def make_dir(dir_path):
    home_dir = os.path.expanduser ('~')
    new_dir  = home_dir + '/' + dir_path
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
        return True
    return False

def get_absoulte_dir(dir_path):
    home_dir = os.path.expanduser ('~')
    new_dir  = home_dir + '/' + dir_path
    return new_dir


    
