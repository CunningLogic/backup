#!/usr/bin/python
#coding:utf-8

__author__ = 'laopangzhang'

baklist = [
 {
     "remote_ip":"10.45.8.229",
     "srcdir":"/data2/backup-nginx/AWS-10.45.8.229-vg012/",
     "destdir":"/backup/",
     "key":"/home/superman/.ssh/superman_rsa",
     "username":"superman",

 },

 {
     "remote_ip":"10.45.8.229",
     "srcdir":"/is2_data/AWS-10.203.163.174-vg014/",
     "destdir":"/backup/",
     "key":"/home/superman/.ssh/superman_rsa",
     "username":"superman"
 },

]


AWS_S3 = {"Bucket":"backup-data-dji","dir":"/backup/",}

needEncry = '.zip'

