#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os

class SouGou():
    CONFIG_RCD_GZ_URL ='http://dl.bizhi.sogou.com/ini/config.rcd.1.1b.ini.gz?time=1374480774&h=D5950D793073C43D32066B4BB8126F82&v=1.5.0.0921&r=0000_sogou_wallpaper_1.5&rreal=0000_sogou_wallpaper_1.5&rov=6.1.7601_1_1&ov=6.1.7601_1.0_1_256_1&widht=1920&height=1080'
    DOWNLOAD_URL='http://download.bizhi.sogou.com/download.php?id=340459&width=1920&height=1080&src=1&h=D5950D793073C43D32066B4BB8126F82&v=1.5.0.0921&r=0000_sogou_wallpaper_1.5&rreal=0000_sogou_wallpaper_1.5&rov=6.1.7601_1_1&ov=6.1.7601_1.0_1_256_1'
    RES_DIR = '.wallpaper'
    WALLPAPER_DIR =  RES_DIR +'/wallpaper'
    RES_CACHE=None 

    
    def __init__(self):
        make_dir(self.RES_DIR)
        make_dir(self.WALLPAPER_DIR)
        pass

    def getResContent(self):
        if self.RES_CACHE != None:
            return self.RES_CACHE
        gz_res = get_content_from_url(self.CONFIG_RCD_GZ_URL)
        tfile = file("/home/wjj/"+self.RES_DIR+"/config.ini.gz",'wb')
        #tfile = tempfile.NamedTemporaryFile(delete= False)
        tfile.write(gz_res)
        tfile.close()
        plain_res = readGzip(tfile.name)
        #os.unlink(tfile.name)

        self.RES_CACHE =  json.loads(unicode(plain_res,'iso-8859-1').replace('\r\n', '\\r\\n'))

        return self.RES_CACHE
    
        
    def downloadImg(self):
        img_res = get_content_from_url(self.DOWNLOAD_URL)
        f = file(get_absoulte_dir(self.WALLPAPER_DIR+'/test.jpeg'),'wb').write(img_res)

    def downloadImageAndSave(self, imageUrl):
        #imageUrl = 'http://imgstore.cdn.sogou.com/app/a/11220002/349351_s_90_2.webp'
        img_res = get_content_from_url(imageUrl)
        print imageUrl
        temp = imageUrl.split("/")
        temp.reverse()
        fileName= temp[0]
        filePath = get_absoulte_dir(self.WALLPAPER_DIR+'/'+fileName)
        print filePath
        f = file(filePath,'wb').write(img_res)
        new_file_path = filePath + '.png'
        convert_webp_to_png(filePath, new_file_path)
        return filePath
        

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
    while i < 50:
        sg.downloadImageAndSave(img_list[i])
        i = i + 1 
        
    #sg.downloadImageAndSave(sg.getImgList())
    
    
        
        
        
