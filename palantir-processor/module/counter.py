#!/usr/bin/env python

import os, sys, re

from util import misc

# Reference
referenceLoc = "/groups/zuber/zubarchive/USERS/tobias/references/hg19"

def getAvailableAlignments(root, experiment, build):
    alignments = []

    for subdir, dirs, files in os.walk(root):
        for file in files:
            fullPath = os.path.join(subdir, file)
            dir = os.path.split(fullPath)[0]
            file = os.path.split(fullPath)[1]
            search = re.search("\.bam$", file, flags=0)
        
            if (build == getSampleBuild(dir) and search ) :
                alignments.append(os.path.join(subdir, file))
            
    return alignments
            
def count(root, experiment, reference, threads):
    
    # Load featureCounts module
    misc.run("module load subread", log=sys.stderr,verbose = False, dry = False)
    
    build = getReferenceBuild(reference)
    alignments = getAvailableAlignments(root, experiment, build)
    
    for alignment in alignments:
        dir = os.path.split(alignment)[0]
        misc.safeCreateDir(os.path.join(dir, reference))
        outFile = os.path.join(dir, reference, misc.removeExtension(os.path.split(alignment)[1]) + ".feature.count")
        command = "featureCounts -b -a " + os.path.join(referenceLoc,reference) + " -i " + alignment + " -o " + outFile + " -T " + str(threads)
        misc.run(command, log=sys.stderr,verbose=False,dry=False)
            
def getSampleBuild(dir):
    build = os.path.split(os.path.split(os.path.split(dir)[0])[0])[1]
    return build
            
def getReferenceBuild(reference):
    build = os.path.basename(os.path.split(os.path.join(referenceLoc, reference))[0])
    return(build)