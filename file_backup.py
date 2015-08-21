#!/usr/bin/python
#coding:utf-8

__author__ = 'laopangzhang'

import os
from conf import *
from zf import *
from jinja2 import Template
import datetime
import socket
import struct
import fcntl
import logging
import subprocess



def today(str):
    now = datetime.datetime.now()
    return now.strftime(str)


def setsrcconf(srclist):
    for ele in srclist:
        template = Template(ele.get('dest'))
        ele['dest'] = template.render(date_today = today(date_now))

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])




def SetBackupDir(NIC):
    IP = get_ip_address(NIC)
    HN = socket.gethostname()
    template = Template(backuphome)
    dir = template.render(ip = IP,host = HN)
    path = dstpath + dir + '/'
    if not os.path.exists(path):
        if not (os.system('mkdir -p' + ' ' + path) == 0):
            logging.error("can't create dir of destination")
            exit(100)
	else:
    	  return path
    else:
      return path



def InitialMysql():
    sqllist=[]
    try:
        dbs = subprocess.Popen(Getdatabase, shell=True, stdout=subprocess.PIPE)
        for line in dbs.stdout.readlines():
	        line = line.strip('\n')
	        sqllist.append(line)
    except:
        logging.error("Get database from db failed!!")
    return sqllist



def BakDB():
    logging.info("Starting dump MySQL data .....")
    dbs = InitialMysql()
    for db in dbs:
        template = Template(mysql['filename'])
        dstfile = template.render(DB_name = db,date_today=today(date_now))
        dbpath = backuphome  + dstfile
	if mysql['binlog'] == '0':
          DumpDB =  "%s -u %s --password='%s' -h %s  %s > %s" % (
               MySQLDUMPCMD,mysql['user'],mysql['pass'],mysql['ip'],db,dbpath)
        else:
          DumpDB =  "%s -u %s --password='%s' -h %s --master-data=%s %s > %s" % (
               MySQLDUMPCMD,mysql['user'],mysql['pass'],mysql['ip'],mysql['binlog'],db,dbpath)
        try:
            proc = subprocess.Popen(DumpDB, shell = True)
            if not (proc.wait() == 0):
                logging.error(db + " " + "export failed!")
            else:
                logging.info(db + " " + "is exported to" + " " + dbpath)
                if zip_file(dbpath):
                    logging.info("zip sql file" + dbpath + "successfully")
                else:
                    logging.error("zip sql file" + dbpath + "failed!")
        except:
            logging.error("MySQL Connectons is error!")
	#logging.info("dumpSQL=" + " " + DumpDB)

          

def doBackup(srclist):
    for src in srclist:
        if not (os.path.exists(src.get('source'))):
            logging.warn("file name" + src.get('source') + "is not exists!")
            continue
        elif (src.get('dest').find('.tar.gz') != -1):
            cmd = 'tar zcvf' + ' ' + backuphome + src.get('dest') + ' ' + src.get('source')
            logging.info(cmd)
            if (os.system(cmd) == 0):
                logging.info("tar file sucessful!")
            else:
                logging.error("tar file failed")
        else:
            cmd = 'cp' + ' ' + src.get('source') + ' ' + backuphome + src.get('dest')
            logging.info(cmd)
            if (os.system(cmd) == 0):
                logging.info("cp file sucessfull")
            else:
                logging.error("cp file failed")

def delbackupfile(dir,days,exfile='*'):
    if os.path.exists(dir) and days >=1 and days <=100:
        #find .  -name '*py' -mtime +1 -exec ls -la {} \;
        delcmd = "find %s -name '%s' -type f -ctime +%s  -exec rm -fr {} \;" % (dir,exfile,days)
        logging.info(delcmd)
        if (os.system(delcmd) == 0):
            logging.info("delete outdate file is ok!")
            return True
        else:
            logging.error("delete outdate file is error!")
            return False
    else:
        return False




if __name__ == '__main__':
    setsrcconf(srclist)
    backuphome = SetBackupDir(ip)
    logging.info(backuphome)
    logging.info(srclist)
    doBackup(srclist)
    if not mysql['isBackup']:
        logging.info("does not need to backup DB!")
    else:
        BakDB()
    delbackupfile(backuphome,retain)




