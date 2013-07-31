#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
from util import make_dir ,get_absoulte_dir
from netutil import get_content_from_url
import util
import netutil

class SouGou():
    CONFIG_RCD_GZ_URL ='http://dl.bizhi.sogou.com/ini/config.rcd.1.1b.ini.gz?time=1374480774&h=D5950D793073C43D32066B4BB8126F82&v=1.5.0.0921&r=0000_sogou_wallpaper_1.5&rreal=0000_sogou_wallpaper_1.5&rov=6.1.7601_1_1&ov=6.1.7601_1.0_1_256_1&widht=1920&height=1080'
    DOWNLOAD_URL='http://download.bizhi.sogou.com/download.php?id=%s&width=%s&height=%s&src=1&h=D5950D793073C43D32066B4BB8126F82&v=1.5.0.0921&r=0000_sogou_wallpaper_1.5&rreal=0000_sogou_wallpaper_1.5&rov=6.1.7601_1_1&ov=6.1.7601_1.0_1_256_1'
    RES_DIR = '.wallpaper'
    WALLPAPER_DIR =  RES_DIR +'/wallpaper'
    LARGE_DIR  =  WALLPAPER_DIR + '/large'
    RES_CACHE=None 

    
    def __init__(self):
        make_dir(self.RES_DIR)
        make_dir(self.WALLPAPER_DIR)
        make_dir(self.LARGE_DIR    )
        pass

    def getResContent(self):
        if self.RES_CACHE != None:
            return self.RES_CACHE
        gz_res = get_content_from_url(self.CONFIG_RCD_GZ_URL)
        tfile = file("/home/wjj/"+self.RES_DIR+"/config.ini.gz",'wb')
        #tfile = tempfile.NamedTemporaryFile(delete= False)
        tfile.write(gz_res)
        tfile.close()
        plain_res = util.readGzip(tfile.name)
        #os.unlink(tfile.name)

        self.RES_CACHE =  json.loads(unicode(plain_res,'iso-8859-1').replace('\r\n', '\\r\\n'))

        return self.RES_CACHE
    
        
    def downloadLargeImg(self, imgId, width, height):
        img_url = self.DOWNLOAD_URL % (imgId, width, height)
        img_res = get_content_from_url(img_url)
        large_img_save_dir =  util.get_absoulte_dir(self.LARGE_DIR+'/%s' % imgId)
        f = file(large_img_save_dir,'wb').write(img_res)
        return large_img_save_dir

    def downloadImageAndSave(self, imageUrl):
        #imageUrl = 'http://imgstore.cdn.sogou.com/app/a/11220002/349351_s_90_2.webp'
        print imageUrl
        temp = imageUrl.split("/")
        temp.reverse()
        fileName= temp[0]
        filePath = get_absoulte_dir(self.WALLPAPER_DIR+'/'+fileName)
        print 'filePath', filePath
        new_file_path = filePath + '.png'
        #png_file = file(new_file_path,'r')
        if os.path.isfile(new_file_path):
            print 'exist ,skip download \n'
        else:
            img_res = get_content_from_url(imageUrl)
            f = file(filePath,'wb').write(img_res)
            util.convert_webp_to_png(filePath, new_file_path)
        return new_file_path
        

    def getImgList(self):
        jres = self.getResContent()
        root_site= jres['root_site']['root_site']
        wallpaper = jres['wallpaper']
        img_list =[]
        for w in wallpaper:
            img_list.append(root_site+w['ae'])
            
        #return root_site+wallpaper[0]['ae']
        return img_list


if __name__ == '__main__':
    sg = SouGou()
    img_list =  sg.getImgList()
    for img in img_list:
        print img
    i = 0 
    while i < 100:
        sg.downloadImageAndSave(img_list[i])
        i = i + 1 
        
    #sg.downloadImageAndSave(sg.getImgList())
    
    
        
        
        
