#!/usr/bin/env python
from ruffus import *
import sys
import os
import time
import datetime
import drmaa
from omics_pipe.utils import *
from omics_pipe.parameters.default_parameters import default_parameters
p = Bunch(default_parameters)
os.chdir(p.WORKING_DIR)
now = datetime.datetime.now()
date = now.strftime('%Y-%m-%d %H:%M') 
print p
for step in p.STEPS:
    vars()['inputList_' + step] = []
    for sample in p.SAMPLE_LIST:
        vars()['inputList_' + step].append([sample, '%s/%s_%s_completed.flag' % (p.FLAG_PATH, step, sample)])
    print vars()['inputList_' + step]
from omics_pipe.modules.DESeq2  import DESeq2
@parallel(inputList_run_DESeq2)
@check_if_uptodate(check_file_exists)
def run_DESeq2(sample, DESeq2_flag):
    DESeq2(sample, DESeq2_flag)
    return
@parallel(inputList_last_function)
@check_if_uptodate(check_file_exists)
@follows(run_DESeq2)
def last_function(sample, last_function_flag):
    print 'PIPELINE HAS FINISHED SUCCESSFULLY!!! YAY!' 
    stage = 'last_function' 
    flag_file = '%s/%s_%s_completed.flag' % (p.FLAG_PATH, stage, sample)
    open(flag_file, 'w').close()
    return
if __name__ == '__main__':
    pipeline_run(p.STEP, multiprocess = p.PIPE_MULTIPROCESS, verbose = p.PIPE_VERBOSE, gnu_make_maximal_rebuild_mode = p.PIPE_REBUILD)
