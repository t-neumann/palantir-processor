#!/usr/bin/env python

from __future__ import print_function

import os, sys, re, shutil

from util import misc

# Reference
referenceLoc = "/groups/zuber/zubarchive/USERS/tobias/references/gtf/"

def getAvailableAlignments(root, experiment, build, verbose, log):
    alignments = []

    for subdir, dirs, files in os.walk(root):
        for file in files:
            fullPath = os.path.join(subdir, file)
            dir = os.path.split(fullPath)[0]
            file = os.path.split(fullPath)[1]
            search = re.search("\.bam$", file, flags=0)
        
            if (build == getSampleBuild(dir) and search ) :
                if (verbose): 
                    print("Matched build detected:\t" + os.path.join(subdir, file), file=log)
                alignments.append(os.path.join(subdir, file))
            
    return alignments
            
def count(root, experiment, reference, threads, verbose = False, log = sys.stdout, force = False, dry = True):
    
    # Load featureCounts module
    # misc.run("module load subread", log=sys.stderr,verbose = False, dry = False)
    
    build = getReferenceBuild(reference)
            
    if (verbose) :
        print ("Genome build of reference detected is:\t" + build, file=log)
    alignments = getAvailableAlignments(root, experiment, build, verbose, log)
    
    for alignment in alignments:
        dir = os.path.split(alignment)[0]
        ref = os.path.basename(reference)
        if (force) :
            shutil.rmtree(os.path.join(dir, ref))
        misc.safeCreateDir(os.path.join(dir, ref))
        outFile = os.path.join(dir, ref, misc.removeExtension(os.path.split(alignment)[1]) + ".feature.count")
        
        command = "~/bin/subread-1.5.0-p1-source/bin/featureCounts -a " + os.path.join(referenceLoc,reference)+ " -o " + outFile + " -T " + str(threads)  + " " + alignment 
        if (not os.path.exists(outFile)) : 
            misc.run(command, log, verbose, dry)
            
def getSampleBuild(dir):
    build = os.path.split(os.path.split(os.path.split(dir)[0])[0])[1]
    return build
            
def getReferenceBuild(reference):
    build = os.path.basename(os.path.split(os.path.join(referenceLoc, reference))[0])
    return(build)