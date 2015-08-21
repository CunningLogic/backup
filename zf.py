#!/usr/bin/python
#coding:utf-8


__author__ = 'laopangzhang'


import os,os.path
import zipfile

def explor(dirname):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
    print filelist

def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        zf.write(tar,arcname)
    zf.close()


def zip_file(path):
    if not os.path.exists(path):
        return False
    else:
        try:
            zf = zipfile.ZipFile(path + ".zip", "w", zipfile.zlib.DEFLATED,True)
            zf.write(path)
            zf.close()
            os.remove(path)
            return True
        except:
            return False






if __name__ == '__main__':
    pass