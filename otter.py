#!/usr/bin/python
#coding:utf-8
__author__ = 'laopangzhang'

#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
#Filename:urllib2-header.py

import urllib2
import sys,datetime
from bs4 import BeautifulSoup
from sendsms import *
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='sms.log',
                filemode='a')

url= "http://120.26.45.44:8080/pipeline_list.htm?channelId=2"

otter = "http://120.26.45.44:8080/"

extime = ['22','23','0-8']
tol = 3600


def Gettime():
    timelist = []

    send_headers = {
        'Host':'120.26.45.44',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection':'keep-alive'
    }
    req = urllib2.Request(url,headers=send_headers)
    r = urllib2.urlopen(req)
    html =  r.read()
    receive_header = r.info()
    # sys.getfilesystemencoding()
    html = html.decode('utf-8','replace').encode(sys.getfilesystemencoding())
    soup = BeautifulSoup(html)
    rows = soup.findAll('tr')

    lastupdate = soup.findAll('td')[16].text
    latency = soup.findAll('td')[15].text
    timelist.append(lastupdate)
    timelist.append(latency)
    return timelist


def GetHour(time):
    if (time.find('h') != -1):
        return time[0:time.find("h")].strip()
    else:
        return 0



def GetMIN(time):
    if (time.find('m') != -1):
        return time[0:time.find("m")].strip()
    else:
        return 0



def GetMIN(time):
    if (time.find('m') != -1):
        return time[time.find("h") + 1 :time.find("m")].strip()
    else:
        return 0

def GetSec(time):
    if time.find('m'):
        return time[time.find("m") + 1 :time.find(".")].strip()
    else:
        return 0




def trantosec(time):
    Hour = GetHour(time)
    Min = GetMIN(time)
    Sec = GetSec(time)

    latency = int(Hour) * 60 * 60 + int(Min) * 60 + int(Sec)
    return latency



if __name__ == '__main__':
    cur = datetime.datetime.now().hour
    for i in extime:
        if (i.find('-') != -1):
            timeseg = i.split('-')
            if not (timeseg[0] < timeseg[1]):
                exit(100)
            else:
                if cur >= int(timeseg[0]) and cur <= int(timeseg[1]):
                    exit(99)
        else:
            if cur == int(i):
                exit(99)

    timelist = Gettime()
    latency = timelist[1]
    last = timelist[0]
    d = datetime.datetime.strptime(last,'%Y-%m-%d %H:%M:%S')
    diff = datetime.datetime.now() - d
    updatediff =  diff.seconds
    latency =  trantosec(latency)
    #print updatediff,latency
    if updatediff >= tol or latency >= tol:
        tpl_value = '#otter#=' + otter + '&#latency#=' + str(latency) + '&#last#=' + last
        logging.info(tpl_send_sms(apikey, tpl_id, tpl_value, mobile))
