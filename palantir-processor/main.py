#!/usr/bin/env python

#########################################################################
# Main routine for the SLAMdunk analyzer
#########################################################################
# Imports
#########################################################################

from __future__ import print_function
import sys, os, re
import subprocess

import shutil

from module import creator, counter
from util import misc

from argparse import ArgumentParser, RawDescriptionHelpFormatter
    
from os.path import basename

########################################################################
# Global variables
########################################################################

# Sampleurl = http://gecko:9100/sequencedSamples/group/ + group
sampleUrl = "http://gecko:9100/sequencedSamples/group"
# Alignmenturl = http://gecko:9100/alignments/group/ + group + /text
alignmentUrl = "http://gecko:9100/alignments/group"

logToMainOutput = True

mainOutput = sys.stderr

########################################################################
# Functions
########################################################################

def message(msg):
    print(msg, file=mainOutput)

def getLogFile(path):
    if(logToMainOutput):
        return mainOutput
    else:
        log = open(path, "a")
        return log
    
def closeLogFile(log):
    if(not logToMainOutput):
        log.close()

    
########################################################################
# Argument parsing
########################################################################

# Info
usage = "palantir-processor for analyzing NGS data and preparing it for palantir import"
version = "1.0"

# Main Parser
parser = ArgumentParser(description=usage, formatter_class=RawDescriptionHelpFormatter, version=version)
parser.add_argument("-b", "--verbose", action='store_true', dest="verbose", help="Verbose output")

subparsers = parser.add_subparsers(help="", dest="command")

# query command

queryparser = subparsers.add_parser('query', help='Query Queue API')
queryparser.add_argument("-g", "--group", type=str, required=True, dest="group", help="Group to retrieve data from")
queryparser.add_argument("-u", "--user", type=str, required=True, dest="user", help="Username")
queryparser.add_argument("-p", "--password", type=str, required=True, dest="password", help="Password")

# prepare command

prepareparser = subparsers.add_parser('prepare', help='Retreive data and prepare folder structure')
prepareparser.add_argument('experiments', action='store', help='Experiment(s)' , nargs="+")
prepareparser.add_argument("-r", "--rootDirectory", type=str, required=True, dest="root", help="Root directory for data preparation prepare data to")
prepareparser.add_argument("-g", "--group", type=str, required=True, dest="group", help="Group to retrieve data from")
prepareparser.add_argument("-u", "--user", type=str, required=True, dest="user", help="Username")
prepareparser.add_argument("-p", "--password", type=str, required=True, dest="password", help="Password")
prepareparser.add_argument("-f", "--force", action='store_true', dest="force", help="Force directory creation (updating current data otherwise)")

# count command

prepareparser = subparsers.add_parser('count', help='Count raw data')
prepareparser.add_argument('experiments', action='store', help='Experiment(s)' , nargs="+")
prepareparser.add_argument("-r", "--rootDirectory", type=str, required=True, dest="root", help="Root directory for data preparation prepare data to")
prepareparser.add_argument("-a", "--reference", type=str, required=True, dest="reference", help="Reference to use for counting")
prepareparser.add_argument("-t", "--threads", type=int, required=False, default=1, dest="threads", help="Threads to use")
prepareparser.add_argument("-f", "--force", action='store_true', dest="force", help="Force counting (running on new samples only otherwise)")
prepareparser.add_argument("-d", "--dryrun", action='store_true', dest="dry", help="Dry run")


args = parser.parse_args()

command = args.command

verbose = args.verbose

if (command == "query") :

    log = getLogFile("query.log")
    
    url = '/'.join([alignmentUrl,args.group,"text"])
    
    data = creator.wgetDataFromUrl(url, args.user, args.password, verbose, log)
    samples = creator.parseAlignmentData(data, verbose, log)
    
    message("Available data for " + args.group + ":\n")
    message("\n".join(samples.keys()))

if (command == "prepare") :
    message("Running prepare") 
    
    log = getLogFile("prepare.log")
    
    if (not os.path.exists(args.root) or not os.path.isdir(args.root)) :
        message("Root directory " + args.root + " does not exist")
        sys.exit(-1)
        
    # Really make sure you want to delete the directory!!
    
    for experiment in args.experiments :
    
        if (args.force) :
            print("Continue deleting directory: " + os.path.join(args.root,experiment))
            choice = raw_input('Y/N?').upper()
            if (choice == "Y") :
                shutil.rmtree(os.path.join(args.root,experiment))
        
        url = '/'.join([alignmentUrl,args.group,"text"])
        
        data = creator.wgetDataFromUrl(url, args.user, args.password, verbose, log)
        samples = creator.parseAlignmentData(data, verbose, log)
        creator.setupFolders(args.root, samples, experiment,verbose, log)
    
if (command == "count") :
    
    message("Running count")
    
    log = getLogFile("count.log")
    
    for experiment in args.experiments :
            
        counter.count(args.root, experiment, args.reference, args.threads, verbose, log, args.force, args.dry)

#########################################################################
# Cleanup
########################################################################
    
sys.exit(0)
