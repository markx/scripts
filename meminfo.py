#!/usr/bin/env python

file=open("/proc/meminfo")
lines=file.readlines()
file.close()

info_needed=['MemTotal','MemFree','Buffers','Cached']
info={}
for line in lines:
    i=line.strip().split(':')
    
    if i[0] in info_needed:
        i[1]=''.join(c for c in i[1] if c.isdigit())
        info[i[0]]=i[1]

mem_free=int(info['MemFree'])+int(info['Buffers'])+int(info['Cached'])
mem_inuse=int(info['MemTotal'])-mem_free
mem_usep=int(int(mem_inuse)/int(info['MemTotal'])*100)

print("{0},{1},{2}%".format(mem_inuse//1024,mem_free//1024,mem_usep))
