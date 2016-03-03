#!/usr/bin/env python
"""OmicsPipe API application.
   linkmodule.py get -r <pipelinerecipesid> -s <stepgroupsid> -t <apitoken> > <custom_script_name>.py
   for example on AWS ~/.local/bin/omics_pipe custom --custom_script_path /home/sgeadmin/omics_sge/omics_pipe/omics_pipe/ --custom_script_name WES_DRAW_OneStepTest /home/sgeadmin/omics_sge/omics_pipe/tests/test_params_WES_GATK_hannah.yaml

Usage:
  linkmodule.py get -r <pipelinerecipesid> -s <stepgroupsid> -t <apitoken>
  linkmodule.py (-h | --help)
  linkmodule.py (-v | --version)

Options:
  -r --pipelinerecipesid <pipelinerecipesid> input pipelinerecipe id
  -s --stepgroupsid <stepgroupsid> input stepgroups id
  -t --apitoken <apitoken> input api token
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
url_stepgroups = 'http://aws1niagads.org:8000/stepgroups/' + arguments['--stepgroupsid']
url_steps = 'http://aws1niagads.org:8000/steps/'
url_pipelinerecipes = 'http://aws1niagads.org:8000/pipelinerecipes/' + arguments['--pipelinerecipesid']
token = arguments['--apitoken']
headers = {'Authorization': '%s' % token}
request_stepgroups = Request(url_stepgroups, headers=headers)
request_steps = Request(url_steps, headers=headers)
request_pipelinerecipes = Request(url_pipelinerecipes, headers=headers)
response_stepgroups = urlopen(request_stepgroups)
response_steps = urlopen(request_steps)
response_pipelinerecipes = urlopen(request_pipelinerecipes)
data_stepgroups = json.loads(response_stepgroups.read())
data_steps = json.loads(response_steps.read())
data_pipelinerecipes = json.loads(response_pipelinerecipes.read())
step_list = []

def  originalMain():
    print "#!/usr/bin/env python"
    print "from ruffus import *"
    print "import sys"
    print "import os"
    print "import time"
    print "import datetime"
    print "import drmaa"
    print "from omics_pipe.utils import *"
    print "from omics_pipe.parameters.default_parameters import default_parameters"
    print "p = Bunch(default_parameters)"
    print "os.chdir(p.WORKING_DIR)"
    print "now = datetime.datetime.now()"
    print "date = now.strftime('%Y-%m-%d %H:%M') "
    print "print p"

    print "for step in p.STEPS:"
    print "    vars()['inputList_' + step] = []"
    print "    for sample in p.SAMPLE_LIST:"
    print "        vars()['inputList_' + step].append([sample, '%s/%s_%s_completed.flag' % (p.FLAG_PATH, step, sample)])"
    print "    print vars()['inputList_' + step]"

def  loadlastfunctions(step_list):
    print "@parallel(inputList_last_function)"
    print "@check_if_uptodate(check_file_exists)"
    followlist = re.sub("[^\w,]", '', str(step_list))
    print "@follows(" + followlist + ")"
    print "def last_function(sample, last_function_flag):"
    print "    print 'PIPELINE HAS FINISHED SUCCESSFULLY!!! YAY!' "
    print "    stage = 'last_function' "
    print "    flag_file = '%s/%s_%s_completed.flag' % (p.FLAG_PATH, stage, sample)"
    print "    open(flag_file, 'w').close()"
    print "    return"
    print "if __name__ == '__main__':"
    print "    pipeline_run(p.STEP, multiprocess = p.PIPE_MULTIPROCESS, verbose = p.PIPE_VERBOSE, gnu_make_maximal_rebuild_mode = p.PIPE_REBUILD)"


def  loadSteps(data_stepgroups, data_steps, url_steps, token, headers):
    for num in data_steps:
       if str(num['group']) == arguments['--stepgroupsid']:
          print "from omics_pipe.modules." + str(num['title']) + "  import " + str(num['title']) ## need to check
          #print str(num['title'])
          step = "run_" + str(num['title'])
          step_list.append(step)
          print "@parallel(inputList_" + step + ")"
          print "@check_if_uptodate(check_file_exists)"
          #print num['follows']
          followid = re.sub("[^\d]", '', str(num['follows']))
          #print followid
          if followid != "":
             url_followstep = url_steps + followid
             #print url_followstep
             request_followstep = Request(url_followstep, headers=headers)
             response_followstep = urlopen(request_followstep)
             data_followstep = json.loads(response_followstep.read())
             followstep = data_followstep['title']
             print "@follows(run_" + followstep + ")"
          print "def run_" + str(num['title']) + "(sample, " + str(num['title']) + "_flag):"
          print "    " + str(num['title']) + "(sample, " + str(num['title']) + "_flag)"
          print "    " + "return"

    loadlastfunctions(step_list)



originalMain()
loadSteps(data_stepgroups, data_steps, url_steps, token, headers)
