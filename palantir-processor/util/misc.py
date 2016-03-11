#!/usr/bin/env python

from __future__ import print_function

import sys, os, subprocess

def files_exist(files):
    if (type(files) is list) :
        for f in files:
            if not os.path.exists(f):
                return False
    else:
        if not os.path.exists(files):
            return False
    return True

# remove a (list of) file(s) (if it/they exists)
def removeFile(files):
    if (type(files) is list) :
        for f in files:
            if os.path.exists(f):
                os.remove(f)
    else:
        if os.path.exists(files):
            os.remove(files)
            
# Removes right-most extension from file name
def removeExtension(inFile):
    name = os.path.splitext(inFile)[0]
    ext = os.path.splitext(inFile)[1]
    if(ext == ".gz"):
        name = os.path.splitext(name)[0]
    return name
            
def safeCreateDir(path):
    if (not os.path.exists(path)):
         os.makedirs(path)
    if (not os.path.isdir(path)):
            os.remove(path)
            os.makedirs(path)

def run(cmd, log=sys.stderr, verbose=False, dry=True):
    if(verbose or dry):
        print(cmd, file=log)
    
    if(not dry):
        #ret = os.system(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        lines_iterator = iter(p.stdout.readline, b"")
        for line in lines_iterator:
            print(line, end="", file=log) # yield line
        p.wait();
        if(p.returncode != 0):
            raise RuntimeError("Error while executing command!")