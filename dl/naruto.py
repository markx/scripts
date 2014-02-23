#!/usr/bin/env python

import requests
import re
from urllib.request import urlretrieve
from os import mkdir
from os.path import exists
from time import sleep


s=requests.Session()

s.headers['User-Agent']='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'
if not exists("naruto"):
    mkdir("naruto")

url="http://manhua.fzdm.com/1/"

for chapter in range(663,664):
    content= s.get("%s%d/index_0.html" %(url, chapter)).content.decode()
    re.findall('<img src="(http://s2.fzdm.org/\d+/\d+/\d+.jpg)" id="mhpic"', content)
    pic0=re.findall('<img\ssrc="(http://.+fzdm\.org.+\.jpg).*id="mhpic"', content)[0]
    if pic0:
        if not exists("naruto/%d-%s.jpg" %(chapter, '1')):
            c=s.get(pic0).content
            with open("naruto/%s-1.jpg" %chapter, "wb") as f:
                print("downloading "+pic0)
                f.write(c)
                print("%d %s downloaded!\n" %(chapter, '1'))

        else:
            print("%d-%s.jpg exists!" %(chapter, '1'))


        indexall=re.findall('<a href="index_(\d+)\.html', content)[1:]
        for index in indexall:
            #starting from 1 instead of 0
            index=str(int(index)+1)
            if exists("naruto/%d-%s.jpg" %(chapter, index)):
                print("%d-%s.jpg exists!" %(chapter, index))
                continue
            c= s.get("%s%d/index_%s.html" %(url, chapter, index)).content.decode()
            pic=re.findall('<img\ssrc="(http://.+fzdm\.org.+\.jpg).*id="mhpic"', c)[0]
            if pic:
                print("downloading "+pic+"")
                c=s.get(pic).content
                with open("naruto/%d-%s.jpg" %(chapter, index), "wb") as f:
                    f.write(c)
                print("%d %s downloaded!\n" %(chapter, index))
    
            sleep(0.3)
