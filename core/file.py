#! /user/bin/python
# coding:UTF-8

import shutil

def ReadFromFile(file):
    content = ''
    try:
        f = open(file, 'r')
    except:
        return ''
    try:
        content = f.read()
    except:
        return ''
    finally:
        f.close()
    return content

def WriteToFile(file, content):
    try:
        f = open(file, 'w')
    except:
        return False
    try:
        f.write(content)
    except:
        return False
    finally:
        f.close()
    return True

def SaveFileFromSrcToDst(src, dst):
    # 拷贝保存某个文件
    try:
        shutil.copy(src, dst)
        return True
    except:
        return False