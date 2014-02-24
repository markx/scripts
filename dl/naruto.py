#!/usr/bin/env python

import requests
import re
from os import mkdir
from os.path import exists
from time import sleep
import argparse

def main(start, end=None):
    s=requests.Session()
    s.headers['User-Agent']='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'

    if not exists("naruto"):
        mkdir("naruto")
    
    url="http://manhua.fzdm.com/1/"
    if end==-1:
        '''get the lastest chapter'''
        try:
            content= s.get(url).content.decode()
            end=re.findall(r'a\shref\=\"(\d{3,})/\"\stitle',content)[0]
            end=int(end)
            print("The latest chapter is %d" %end)
        except Exception as e:
            print("cannot get the latest chapter, set it manully")
            print(e)
            exit()
    
    print("downloading from %d to %d" %(start, end))
    sleep(2)
    for chapter in range(start,end+1):
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
    
    
            indexall=re.findall('<a href=\"index_(\d+)\.html\">', content)
            for index in indexall:
                index=int(index)
                if exists("naruto/%d-%d.jpg" %(chapter, index+1)):
                    print("%d-%d.jpg exists!" %(chapter, index+1))
                    continue
                c= s.get("%s%d/index_%d.html" %(url, chapter, index)).content.decode()
                pic=re.findall('<img\ssrc="(http://.+fzdm\.org.+\.jpg).*id="mhpic"', c)[0]
                if pic:
                    print("downloading "+pic+"")
                    c=s.get(pic).content
                    with open("naruto/%d-%d.jpg" %(chapter, index+1), "wb") as f:
                        f.write(c)
                    print("%d %s downloaded!\n" %(chapter, index+1))
        
                sleep(0.3)


if __name__ == "__main__":
    arg=argparse.ArgumentParser(description="Download naruto")
    arg.add_argument('start', nargs='?',default=630, type=int, help="start chapter")
    arg.add_argument('end' , nargs='?',default=-1, type=int ,help="end chapter")
    args=arg.parse_args()
    main(args.start, args.end)
