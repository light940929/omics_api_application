#!/usr/bin/env python
from omics_pipe.parameters.default_parameters import default_parameters
from omics_pipe.utils import *
p = Bunch(default_parameters)
def bwa_mem_draw(sample,bwa_mem_draw_flag):
    '''BWA aligner with BWA-MEM algorithm.
    input:
         FASTQ
    output:
          BAM
    citation:
          
    link:
          
    parameters from parameters file:
          BWA_RESULTS, TEMP_DIR, RG_STR, BWA_VERSION, BWA_INDEX, sample, RAW_DATA_DIR, BWA_OPTIONS, COMPRESSION
    '''
    spawn_job(jobname = 'bwa_mem_draw', SAMPLE = sample, LOG_PATH = p.LOG_PATH, RESULTS_EMAIL = p.RESULTS_EMAIL, SCHEDULER = p.SCHEDULER, walltime = '240:00:00', queue = p.QUEUE, nodes = 1, ppn = 4, memory = '8gb', script = '/home/hannah/Omics_pipe_api/omics_sge/omics_pipe/omics_api/uploads/scripts/bwa_drmaa_PE_DRAW.sh', args_list = [p.BWA_RESULTS,p.TEMP_DIR,p.RG_STR,p.BWA_VERSION,p.BWA_INDEX,p.sample,p.RAW_DATA_DIR,p.BWA_OPTIONS,p.COMPRESSION])
    job_status(jobname = 'bwa_mem_draw', resultspath = p.BWA_RESULTS, SAMPLE = sample, outputfilename = /home/hannah/Omics/WES/test_sorted.bam, FLAG_PATH = p.FLAG_PATH)
    return
if __name__ == '__main__':
    bwa_mem_draw(sample,bwa_mem_draw_flag)
    sys.exit(0)
