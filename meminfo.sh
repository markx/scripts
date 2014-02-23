#!/usr/bin/bash

cat /proc/meminfo| awk  'BEGIN{total=0;free=0;use=0} {if($1 ~ /MemTotal/) total=$2/1024; else if($1 ~ /MemFree|Buffers|Cached/) free+=$2/1024} END{use=total-free; printf"%d %d %d%",use,total,use/total*100}'


