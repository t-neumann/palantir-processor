#!/usr/bin/env python

import os, urllib3, re

from util import misc

def linkBamFile(source, destination):
    contents = os.listdir(os.path.split(source)[0])
    
    toLink = source
    
    for file in contents:
        search = re.search(".*uniq.*.bam$", file, flags=0)
        if search:
            toLink = os.path.join(os.path.split(source)[0],file)
        
    if (not os.path.exists(os.path.join(destination,os.path.split(toLink)[1]))) :
        os.symlink(toLink, os.path.join(destination,os.path.split(toLink)[1]))
    if (not os.path.exists(os.path.join(destination,os.path.split(toLink)[1]) + ".bai")) :
        # TODO: Check if bai is even available
        os.symlink(toLink + ".bai", os.path.join(destination,os.path.split(toLink)[1]) + ".bai")

def setupFolders(rootDir, samples, experiment):
    misc.safeCreateDir(os.path.join(rootDir,experiment))
    #for experiment in samples.keys():
    #    safeCreateDir(os.path.join(rootDir,experiment))
    for build in samples[experiment].keys():
        misc.safeCreateDir(os.path.join(rootDir,experiment, build))
        for sample in samples[experiment][build].keys():
            misc.safeCreateDir(os.path.join(rootDir,experiment, build, sample))
            for alignment in samples[experiment][build][sample].keys():
                misc.safeCreateDir(os.path.join(rootDir,experiment, build, sample,alignment))
                if (os.path.exists(samples[experiment][build][sample][alignment]['bam'])):
                    src = samples[experiment][build][sample][alignment]['bam']
                    dst = os.path.join(rootDir,experiment, build, sample,alignment)
                    linkBamFile(src, dst)

def wgetDataFromUrl(url, user, password):
    http = urllib3.PoolManager()
    headers = urllib3.util.make_headers(basic_auth=user + ":" + password)
    r = http.request('GET',url,headers=headers)

    return r.data.split("\n")

def parseAlignmentData(data):
    
    dict = {}
    
    columns = extractColumns(data[0])

    for i in range(1,len(data)):
        fields = data[i].split("\t")

        if (not fields[columns["experimentType"]] in dict.keys()):
            dict[fields[columns["experimentType"]]] = {}
        if (not fields[columns["build"]] in dict[fields[columns["experimentType"]]].keys()):
            dict[fields[columns["experimentType"]]][fields[columns["build"]]] = {}
        if (not fields[columns["sampleId"]] in dict[fields[columns["experimentType"]]][fields[columns["build"]]].keys()):
            dict[fields[columns["experimentType"]]][fields[columns["build"]]][fields[columns["sampleId"]]] = {}
        if (not fields[columns["analysisDate"]] in dict[fields[columns["experimentType"]]][fields[columns["build"]]][fields[columns["sampleId"]]].keys()):
            dict[fields[columns["experimentType"]]][fields[columns["build"]]][fields[columns["sampleId"]]][fields[columns["analysisDate"]]] = {}
        dict[fields[columns["experimentType"]]][fields[columns["build"]]][fields[columns["sampleId"]]][fields[columns["analysisDate"]]]['folder'] = fields[columns["folder"]]
        dict[fields[columns["experimentType"]]][fields[columns["build"]]][fields[columns["sampleId"]]][fields[columns["analysisDate"]]]['bam'] = fields[columns["bam"]]
    
    return(dict)
        
def extractColumns(header):
    
    map = {}
    columns = header.split("\t")
    
    for i in range(0,len(columns)):
        if (columns[i] == "sampleId") :
            map["sampleId"] =  i
        if (columns[i] == "experimentType") :
            map["experimentType"] =  i
        if (columns[i] == "analysisDate") :
            map["analysisDate"] =  i
        if (columns[i] == "build") :
            map["build"] =  i
        if (columns[i] == "folder") :
            map["folder"] =  i
        if (columns[i] == "bam") :
            map["bam"] =  i
        
    return map