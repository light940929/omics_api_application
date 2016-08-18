#!/usr/bin/env python
from omics_pipe.parameters.default_parameters import default_parameters
from omics_pipe.utils import *
p = Bunch(default_parameters)
def DESeq2(sample,DESeq2_flag):
    '''Gene expressions with DeSeq2
    input:
         TXT
    output:
          OTHER
    citation:
          DeSeq2
    link:
          https://bioconductor.org/packages/release/bioc/html/DESeq2.html
    parameters from parameters file:
          R_HOME, PKG_CONFIG_PATH, LD_LIBRARY_PATH
    '''
    spawn_job(jobname = 'DESeq2', SAMPLE = sample, LOG_PATH = p.LOG_PATH, RESULTS_EMAIL = p.RESULTS_EMAIL, SCHEDULER = p.SCHEDULER, walltime = '10:00:00', queue = p.QUEUE, nodes = 1, ppn = 4, memory = '1024', script = '/home/adrian/R_Alex/code/nls_tdp43/wt_deseq2_for_adrian.R', args_list = [p.R_HOME,p.PKG_CONFIG_PATH,p.LD_LIBRARY_PATH])
    job_status(jobname = 'DESeq2', resultspath = p.BWA_RESULTS, SAMPLE = sample, outputfilename = /home/adrian/R_Alex/output/tables, FLAG_PATH = p.FLAG_PATH)
    return
if __name__ == '__main__':
    DESeq2(sample,DESeq2_flag)
    sys.exit(0)
