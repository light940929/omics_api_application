#!/usr/bin/env python
"""OmicsPipe API application for choosing our standard pipeline and template to build a new template.
   buildtemplate.py get -p <pipelinesid> -i <ingredientgroupsid> -t <templatesid>  -u <username> -e <useremail> -a <apitoken> > <templatename>.yaml

Usage:
  buildtemplate.py get -p <pipelinesid> -i <ingredientgroupsid> -t <templatesid>  -u <username> -e <useremail> -a <apitoken>
  buildtemplate.py (-h | --help)
  buildtemplate.py (-v | --version)

Options:
  -p --pipelinesid <pipelinesid> input pipeline id
  -i --ingredientgroupsid <ingredientgroupsid> input ingredientgroups id
  -t --templatesid <templatesid> input template id
  -u --username <username> input user name
  -e --useremail <useremail> input user email
  -a --apitoken <apitoken> input api token
  -h --help     show this screen
  -v --version     show version and exit
"""
import os
import re
import json
import sys
import getopt
import argparse
from docopt import docopt
from urllib2 import urlopen, Request

arguments = docopt(__doc__, version='0.0.2alpha')

url_pipelines = 'http://aws1niagads.org:8000/pipelines/' + arguments['--pipelinesid']
url_ingredients = 'http://aws1niagads.org:8000/ingredients/'
url_templates = 'http://aws1niagads.org:8000/templates/' + arguments['--templatesid']
url_elements = 'http://aws1niagads.org:8000/elements/'
token = arguments['--apitoken']
headers = {'Authorization': 'Bearer %s' % token}
request_pipelines = Request(url_pipelines, headers=headers)
request_ingredients = Request(url_ingredients, headers=headers)
request_templates = Request(url_templates, headers=headers)
request_elements = Request(url_elements, headers=headers)
response_pipelines = urlopen(request_pipelines)
response_ingredients = urlopen(request_ingredients)
response_templates = urlopen(request_templates)
response_elements = urlopen(request_elements)
data_pipelines = json.loads(response_pipelines.read())
data_ingredients = json.loads(response_ingredients.read())
data_templates = json.loads(response_templates.read())
data_elements = json.loads(response_elements.read())



def  loadPipelines(data_pipelines):
    print "#NAME" + ':\t' + data_pipelines['name']
    print "#DESCRIPTION" + ':\t' + data_pipelines['description']
    print "STEP: last_function"
    print "STEPS: [" + data_pipelines['steps'] + ", last_function]"

def  checkIngredients(data_ingredients):
    status = []
    sample_list = []
    defaultdir = []
    queue = []
    format = []
    scheduler = []

    if data_ingredients == status:
        print "It's null ingredient. Please input ingredients"

    else:
        for num in data_ingredients:
           #print str(num['group'])
           #print arguments['--ingredientgroupsid']
           if str(num['group']) == arguments['--ingredientgroupsid']:
              #print "#TITLE" + str(num['id']) + ':\t' + str(num['title'])
              #print "#SERVER" + ':\t' + str(num['server'])
              #print "#PATH" + ':\t' + str(num['path'])
              if str(num['server']) == "AWS" :
                 tempdir = "TEMP_DIR: /mnt/data"
              elif str(num['server']) == "PMACS" or "CAJAL" or "TESLA" :
                 tempdir = "TEMP_DIR: /home/hanjl/temp"
              else:
                 print "There are no temp direction."
              if str(num['server']) == "AWS" or "TESLA" :
                 queue = "QUEUE: all.q"
                 scheduler = "SCHEDULER: SGE"
                 resources = "RESOURCES: '-q all.q -l nodes=16:ppn=4 -l mem=5gb'"
              elif str(num['server']) == "PMACS" or "CAJAL" :
                 queue = "QUEUE: denovo"
                 scheduler = "SCHEDULER: LSF"
                 resources = "RESOURCES: '-q denovo -R span[ptile=16] -R rusage[mem=6144]'"
              else:
                 print "There are no queue."

              sample = str(num['title'])
              sample_list.append(sample)

              defaultdir = str(num['path'])

              if str(num['format']) == '\wgz':
                 format = "COMPRESSION: 'GZIP'"
              else:
                 formate = "COMPRESSION: 'NONE'"

              if str(num['server']) == "AWS":
                 sumatra_db_path = "SUMATRA_DB_PATH: /mnt/data/genomics/draw-omics-cbd"
                 drmaa_path = "DRMAA_PATH: /opt/sge/lib/lx-amd64/libdrmaa.so"
              else:
                 sumatra_db_path = "SUMATRA_DB_PATH: /home/hanjl/Omics/WES"
                 drmaa_path = "DRMAA_PATH: /home/hanjl/lib/libdrmaa.so"
              print queue
              print "SAMPLE_LIST: " +  str(sample_list)
              print "RAW_DATA_DIR: " + defaultdir
              print "FLAG_PATH: " + defaultdir
              print "LOG_PATH: :" + defaultdir
              print "QC_PATH: " + defaultdir
              print "RESULTS_PATH: " + defaultdir
              print formate
              print scheduler
              print resources
              print drmaa_path
              print sumatra_db_path
              print "SUMATRA_RUN_NAME: default_sumatra_project"

def  checkTemplates(data_templates):
    print "TITLE"  + ':\t' + data_templates['title']
    print "ELEMENTS" + ':\t' + "".join([str(i) for i in data_templates['elements']])


def  checkElements(data_elements, template_id):
    for num in data_elements:
        if str(num['template']) == template_id :
           print str(num['argument']) + ': ' + str(num['default'])

def  checkEnvironment():
     #SERVER_ENV
     print "PIPE_MULTIPROCESS: 1000"
     print "PIPE_REBUILD: 'True'"
     print "PIPE_VERBOSE: 5"
     print "RESULTS_EMAIL: " + arguments['--useremail']
     print "USERNAME: " + arguments['--username']
     print "WORKING_DIR: /home/hannah/omics_sge/omics_pipe/omics_pipe/scripts"
     print "BWA_RESULTS: /mnt/data/genomics/draw-omics-cbd34567"
     print "RG_STR: '@RG	ID:cbd1	SM:cbd1	PL:Illumina	PU:NA	LB:nimblegen	DS:2x100	CN:CBD	DT:2015-05-14'"
     print "RG_STR_PICARD: 'ID=cbd1 SM=cbd1 PL=Illumina PU=NA LB=nimblegen DS=2x100 CN=CBD'"
     print "ENDS: PE"





loadPipelines(data_pipelines)
checkIngredients(data_ingredients)
#checkTemplates(data_templates)
checkElements(data_elements,arguments['--templatesid'])
checkEnvironment()
