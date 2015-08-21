#!/usr/bin/python
#coding:utf-8

__author__ = 'laopangzhang'

from s3conf import  *
from conf import *
import os,getopt,sys,subprocess


def GetFile(dirname,extfn):
    excludefile = '.en'
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                if(name.find(extfn) != -1 and name.find(excludefile) == -1):
                    filelist.append(os.path.join(root, name))
    return filelist



def CollectData(bakhosts):
    for host in bakhosts:
        #scp -rv -i /home/superman/.ssh/superman_rsa superman@www.dji.com:/data2/backup-nginx/AWS-10.45.8.229-vg012 /backup
        ScpCMD = 'scp -rv -i %s %s@%s:%s %s' % (host.get('key'),host.get('username'),
                host.get('remote_ip'),host.get('srcdir'),host.get('destdir'))
        logging.info(ScpCMD)
        proc = subprocess.Popen(ScpCMD,shell = True)
        if (proc.wait() == 0):
            logging.info("successfully file have collected to backup server!")
        else:
            logging.error("Error file have collected to backup server!")

def Syn2S3(s3info):
    SynCMD = 'aws s3 sync %s s3://%s/' %(s3info['dir'],s3info['Bucket'])
    logging.info(SynCMD)
    proc = subprocess.Popen(SynCMD, shell = True)
    if not (proc.wait() == 0):
        logging.info("All file are translated to S3 successfully")
    else:
        logging.error("Transfer is Error!")



#openssl enc -des-ede3-cbc -in test.py -out test.log  -pass pass:111111
def Encryp(filename):
    tarfile = filename + '.en'
    if not os.path.exists(filename):
        return False
    else:
        EncrypCMD = "openssl enc -des-ede3-cbc -in %s -out %s -pass pass:p78pahQi8KE8xJjo85yB" % (filename,tarfile)
        logging.info(EncrypCMD)
        if (os.system(EncrypCMD) == 0):
            logging.info("encrypt the %s successfully" % (filename))
            if os.path.exists(tarfile):
                os.remove(filename)
            else:
                return False
            return True
        else:
            return False

def usage():
    print "s3 -S 'sync to S3' -C 'Collect from every host'  -E 'Encrypt the backup files'"
    print "Version 1.0"

def isobackup():
    logging.info("iso backup is execing ...")
    logging.info("starging CollectData")
    CollectData(baklist)
    logging.info("staring encryp")
    filelist = GetFile(AWS_S3['dir'],needEncry)
    for file in filelist:
        if Encryp(file):
            logging.info("%s is enCryped!" % (file))
        else:
            logging.error("%s crcryp is failed!" % (file))
    logging.info("staring sync to S3")
    Syn2S3(AWS_S3)

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "SCE")
        if len(opts) == 0:
            isobackup()
            exit(0)
        else:
            for op, value in opts:
                if op == "-S":
                    Syn2S3()
                elif op == "-C":
                    CollectData(baklist)
                elif op == "-E":
                    filelist = GetFile(AWS_S3['dir'],needEncry)
                    for file in filelist:
                        if Encryp(file):
                            logging.info("%s is enCryped!" % (file))
                        else:
                            logging.error("%s enCryped is failed!" % (file))
                else :
                    usage()
                    sys.exit(0)
    except getopt.GetoptError,e:
        print e
        usage()



