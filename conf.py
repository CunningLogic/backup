#!/usr/bin/python
#coding:utf-8

__author__ = 'laopangzhang'

'''
config file for backup utilities
just configfile
'''
import logging

ip='eth0'
date_now = '%Y-%m-%d.%H-%M-%S'

srclist = [{'source':'/etc/mysql','dest':'{{ date_today }}.prod.dds.mysql.tar.gz'},
           {'source':'/etc/mysql/my.cnf','dest':'{{ date_today }}.prod.dds.mysql.my.cnf'},
        ];
MysqlClient = 'mysql'
MySQLDUMPCMD = 'mysqldump'


ExcludeDB="'information_schema|performance_schema'"

retain = 7

mysql = { 'ip':'localhost',
        'user':'root',
        'pass':'',
        'binlog':'0',
        'filename':'{{ date_today }}.{{ DB_name }}.prod.store.sql',
        'filelist':'sqllist',
        'isBackup':False
         }

Getdatabase = "%s -u %s --password=%s -h %s -BNe '%s' | grep -Ev %s" % (MysqlClient,
                    mysql['user'], mysql['pass'], mysql['ip'],
                     'show databases',ExcludeDB)





dstpath = '/data/backup-db/'
backuphome = 'UCLOUD-{{ ip }}-{{ host }}'

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='file_backup.log',
                filemode='a')


