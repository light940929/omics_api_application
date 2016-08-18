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
from omics_pipe.modules.bwa_mem_draw  import bwa_mem_draw
@parallel(inputList_run_bwa_mem_draw)
@check_if_uptodate(check_file_exists)
def run_bwa_mem_draw(sample, bwa_mem_draw_flag):
    bwa_mem_draw(sample, bwa_mem_draw_flag)
    return
from omics_pipe.modules.picard_addReadsGroups  import picard_addReadsGroups
@parallel(inputList_run_picard_addReadsGroups)
@check_if_uptodate(check_file_exists)
@follows(run_bwa_mem_draw)
def run_picard_addReadsGroups(sample, picard_addReadsGroups_flag):
    picard_addReadsGroups(sample, picard_addReadsGroups_flag)
    return
from omics_pipe.modules.picard_mark_duplicates  import picard_mark_duplicates
@parallel(inputList_run_picard_mark_duplicates)
@check_if_uptodate(check_file_exists)
@follows(run_picard_addReadsGroups)
def run_picard_mark_duplicates(sample, picard_mark_duplicates_flag):
    picard_mark_duplicates(sample, picard_mark_duplicates_flag)
    return
from omics_pipe.modules.samtools_doFlagStat  import samtools_doFlagStat
@parallel(inputList_run_samtools_doFlagStat)
@check_if_uptodate(check_file_exists)
@follows(run_picard_addReadsGroups)
def run_samtools_doFlagStat(sample, samtools_doFlagStat_flag):
    samtools_doFlagStat(sample, samtools_doFlagStat_flag)
    return
from omics_pipe.modules.GATK_countReads_WES  import GATK_countReads_WES
@parallel(inputList_run_GATK_countReads_WES)
@check_if_uptodate(check_file_exists)
@follows(run_picard_mark_duplicates)
def run_GATK_countReads_WES(sample, GATK_countReads_WES_flag):
    GATK_countReads_WES(sample, GATK_countReads_WES_flag)
    return
from omics_pipe.modules.GATK_localRealignIndel_step1  import GATK_localRealignIndel_step1
@parallel(inputList_run_GATK_localRealignIndel_step1)
@check_if_uptodate(check_file_exists)
@follows(run_picard_mark_duplicates)
def run_GATK_localRealignIndel_step1(sample, GATK_localRealignIndel_step1_flag):
    GATK_localRealignIndel_step1(sample, GATK_localRealignIndel_step1_flag)
    return
from omics_pipe.modules.GATK_localRealignIndel_step2  import GATK_localRealignIndel_step2
@parallel(inputList_run_GATK_localRealignIndel_step2)
@check_if_uptodate(check_file_exists)
@follows(run_GATK_localRealignIndel_step1)
def run_GATK_localRealignIndel_step2(sample, GATK_localRealignIndel_step2_flag):
    GATK_localRealignIndel_step2(sample, GATK_localRealignIndel_step2_flag)
    return
from omics_pipe.modules.GATK_recal_countCovariates  import GATK_recal_countCovariates
@parallel(inputList_run_GATK_recal_countCovariates)
@check_if_uptodate(check_file_exists)
@follows(run_GATK_localRealignIndel_step2)
def run_GATK_recal_countCovariates(sample, GATK_recal_countCovariates_flag):
    GATK_recal_countCovariates(sample, GATK_recal_countCovariates_flag)
    return
from omics_pipe.modules.GATK_recal_tableRecalibration  import GATK_recal_tableRecalibration
@parallel(inputList_run_GATK_recal_tableRecalibration)
@check_if_uptodate(check_file_exists)
@follows(run_GATK_recal_countCovariates)
def run_GATK_recal_tableRecalibration(sample, GATK_recal_tableRecalibration_flag):
    GATK_recal_tableRecalibration(sample, GATK_recal_tableRecalibration_flag)
    return
from omics_pipe.modules.picard_meanQbycycle  import picard_meanQbycycle
@parallel(inputList_run_picard_meanQbycycle)
@check_if_uptodate(check_file_exists)
@follows(run_GATK_recal_tableRecalibration)
def run_picard_meanQbycycle(sample, picard_meanQbycycle_flag):
    picard_meanQbycycle(sample, picard_meanQbycycle_flag)
    return
from omics_pipe.modules.picard_meanQScDis  import picard_meanQScDis
@parallel(inputList_run_picard_meanQScDis)
@check_if_uptodate(check_file_exists)
@follows(run_GATK_recal_tableRecalibration)
def run_picard_meanQScDis(sample, picard_meanQScDis_flag):
    picard_meanQScDis(sample, picard_meanQScDis_flag)
    return
from omics_pipe.modules.picard_hsMetrics  import picard_hsMetrics
@parallel(inputList_run_picard_hsMetrics)
@check_if_uptodate(check_file_exists)
@follows(run_GATK_recal_tableRecalibration)
def run_picard_hsMetrics(sample, picard_hsMetrics_flag):
    picard_hsMetrics(sample, picard_hsMetrics_flag)
    return
from omics_pipe.modules.picard_collectInsertSizeMetrics  import picard_collectInsertSizeMetrics
@parallel(inputList_run_picard_collectInsertSizeMetrics)
@check_if_uptodate(check_file_exists)
@follows(run_GATK_recal_tableRecalibration)
def run_picard_collectInsertSizeMetrics(sample, picard_collectInsertSizeMetrics_flag):
    picard_collectInsertSizeMetrics(sample, picard_collectInsertSizeMetrics_flag)
    return
from omics_pipe.modules.GATK_target_coverage  import GATK_target_coverage
@parallel(inputList_run_GATK_target_coverage)
@check_if_uptodate(check_file_exists)
@follows(run_GATK_recal_tableRecalibration)
def run_GATK_target_coverage(sample, GATK_target_coverage_flag):
    GATK_target_coverage(sample, GATK_target_coverage_flag)
    return
from omics_pipe.modules.GATK_genome_coverage  import GATK_genome_coverage
@parallel(inputList_run_GATK_genome_coverage)
@check_if_uptodate(check_file_exists)
@follows(run_GATK_recal_tableRecalibration)
def run_GATK_genome_coverage(sample, GATK_genome_coverage_flag):
    GATK_genome_coverage(sample, GATK_genome_coverage_flag)
    return
from omics_pipe.modules.GATK_snpcal_unifiedGenotyper  import GATK_snpcal_unifiedGenotyper
@parallel(inputList_run_GATK_snpcal_unifiedGenotyper)
@check_if_uptodate(check_file_exists)
@follows(run_GATK_recal_tableRecalibration)
def run_GATK_snpcal_unifiedGenotyper(sample, GATK_snpcal_unifiedGenotyper_flag):
    GATK_snpcal_unifiedGenotyper(sample, GATK_snpcal_unifiedGenotyper_flag)
    return
from omics_pipe.modules.GATK_variantFiltrationNoMask  import GATK_variantFiltrationNoMask
@parallel(inputList_run_GATK_variantFiltrationNoMask)
@check_if_uptodate(check_file_exists)
@follows(run_GATK_snpcal_unifiedGenotyper)
def run_GATK_variantFiltrationNoMask(sample, GATK_variantFiltrationNoMask_flag):
    GATK_variantFiltrationNoMask(sample, GATK_variantFiltrationNoMask_flag)
    return
from omics_pipe.modules.GATK_variantEval  import GATK_variantEval
@parallel(inputList_run_GATK_variantEval)
@check_if_uptodate(check_file_exists)
@follows(run_GATK_variantFiltrationNoMask)
def run_GATK_variantEval(sample, GATK_variantEval_flag):
    GATK_variantEval(sample, GATK_variantEval_flag)
    return
from omics_pipe.modules.SNPEFF  import SNPEFF
@parallel(inputList_run_SNPEFF)
@check_if_uptodate(check_file_exists)
@follows(run_GATK_snpcal_unifiedGenotyper)
def run_SNPEFF(sample, SNPEFF_flag):
    SNPEFF(sample, SNPEFF_flag)
    return
@parallel(inputList_last_function)
@check_if_uptodate(check_file_exists)
@follows(run_bwa_mem_draw,run_picard_addReadsGroups,run_picard_mark_duplicates,run_samtools_doFlagStat,run_GATK_countReads_WES,run_GATK_localRealignIndel_step1,run_GATK_localRealignIndel_step2,run_GATK_recal_countCovariates,run_GATK_recal_tableRecalibration,run_picard_meanQbycycle,run_picard_meanQScDis,run_picard_hsMetrics,run_picard_collectInsertSizeMetrics,run_GATK_target_coverage,run_GATK_genome_coverage,run_GATK_snpcal_unifiedGenotyper,run_GATK_variantFiltrationNoMask,run_GATK_variantEval,run_SNPEFF)
def last_function(sample, last_function_flag):
    print 'PIPELINE HAS FINISHED SUCCESSFULLY!!! YAY!' 
    stage = 'last_function' 
    flag_file = '%s/%s_%s_completed.flag' % (p.FLAG_PATH, stage, sample)
    open(flag_file, 'w').close()
    return
if __name__ == '__main__':
    pipeline_run(p.STEP, multiprocess = p.PIPE_MULTIPROCESS, verbose = p.PIPE_VERBOSE, gnu_make_maximal_rebuild_mode = p.PIPE_REBUILD)
