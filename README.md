SYNOPSIS
========

The programm `palantir-processor` links NGS data from the [Queue API](http://ngs.vbcf.ac.at/) of the [Next Generation Sequencing Facility](http://www.vbcf.ac.at/facilities/next-generation-sequencing/)
of the Vienna Biocenter Core Facilities to your local filesystem. It runs basic quantification operations (e.g. counting) which act as basis for the import
in the Palantir database.


USAGE
=====

Help for each of the commands of `palantir-processor` can be obtained by calling it with `-h`

query
-----

Given a valid Queue account with required permissions to access group data, you would start with getting an overview of the available experiments:

    palantir-processor query -g group -u user -p password

`palantir-processor` will list all available experiments for the given group

    Available data for group:
    
    ChIP-Seq
    RNA-Seq
    
prepare
-------

Now that you made up your mind of which data to import, a directory tree can be build and the raw data is linked into it.

    palantir-processor prepare [-f] -r ROOT -g GROUP -u USER -p PASSWORD experiments [experiments ...]

Below is the help message describing usage & options:

    positional arguments:
      experiments           Experiment(s)
    
    optional arguments:
      -h, --help            show this help message and exit
      -r ROOT, --rootDirectory ROOT
                            Root directory for data preparation prepare data to
      -g GROUP, --group GROUP
                            Group to retrieve data from
      -u USER, --user USER  Username
      -p PASSWORD, --password PASSWORD
                            Password
      -f, --force           Force directory creation (updating current data
                            otherwise)

  You will have to choose the root directory where the directory tree is created and the respective experiments from `palantir-processor query`
  you want to link. The directory tree can be either forced (deleting old contents) or updated (only linking new samples).
  
count
-----

This module counts read data given a reference using [featureCounts](http://subread.sourceforge.net/) from [WEHI](http://bioinf.wehi.edu.au/featureCounts/).

    palantir-processor count [-h] -r ROOT -a REFERENCE [-t THREADS] [-f] [-d] experiments [experiments ...]

Below is the help message describing usage & options:

    positional arguments:
      experiments           Experiment(s)
    
    optional arguments:
      -h, --help            show this help message and exit
      -r ROOT, --rootDirectory ROOT
                            Root directory for data preparation prepare data to
      -a REFERENCE, --reference REFERENCE
                            Reference to use for counting
      -t THREADS, --threads THREADS
                            Threads to use
      -f, --force           Force counting (running on new samples only otherwise)
      -d, --dryrun          Dry run

A reference has to be selected for counting (described TODO) which will be automatically only used on compatible genome builds. 
Again, counting can be forced (overwriting old files) or updated.
  
INSTALLATION
============

The installation process currently consists of simply checking the projects out from GitHub.

Just do the following:

    git clone https://github.com/t-neumann/palantir-processor.git
    cd palantir-processor
    ./bin/palantir-processor

NOTES
=====

This has been successfully run on Debian GNU/Linux 3.2.0
workstations (both 32-bit and 64-bit machines).

AUTHORS
=======

Tobias Neumann (tobias.neumann@imp.ac.at)

ACKNOWLEDGEMENTS
================

This software was developed at The Research Center for Molecular Pathology, Vienna, Austria.

DISCLAIMER
==========

This software is provided "as is" without warranty of any kind.


March 18, 2016
