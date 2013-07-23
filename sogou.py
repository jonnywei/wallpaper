#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os

class SouGou():
    CONFIG_RCD_GZ_URL ='http://dl.bizhi.sogou.com/ini/config.rcd.1.1b.ini.gz?time=1374480774&h=D5950D793073C43D32066B4BB8126F82&v=1.5.0.0921&r=0000_sogou_wallpaper_1.5&rreal=0000_sogou_wallpaper_1.5&rov=6.1.7601_1_1&ov=6.1.7601_1.0_1_256_1&widht=1920&height=1080'
    DOWNLOAD_URL='http://download.bizhi.sogou.com/download.php?id=340459&width=1920&height=1080&src=1&h=D5950D793073C43D32066B4BB8126F82&v=1.5.0.0921&r=0000_sogou_wallpaper_1.5&rreal=0000_sogou_wallpaper_1.5&rov=6.1.7601_1_1&ov=6.1.7601_1.0_1_256_1'
    RES_DIR = '.wallpaper'
    WALLPAPER_DIR =  RES_DIR +'/wallpaper'
    

    
    def __init__(self):
        make_dir(self.RES_DIR)
        make_dir(self.WALLPAPER_DIR)
        pass

    def getResContent(self):
        gz_res = get_content_from_url(self.CONFIG_RCD_GZ_URL)
        tfile = file("/home/wjj/"+self.RES_DIR+"/config.ini.gz",'wb')
        #tfile = tempfile.NamedTemporaryFile(delete= False)
        tfile.write(gz_res)
        tfile.close()
        plain_res = readGzip(tfile.name)
        #os.unlink(tfile.name)

        return json.loads(unicode(plain_res,'iso-8859-1').replace('\r\n', '\\r\\n'))

    def downloadImg(self):
        img_res = get_content_from_url(self.DOWNLOAD_URL)
        f = file(get_absoulte_dir(self.WALLPAPER_DIR+'/test.jpeg'),'wb').write(img_res)
       
        
        
