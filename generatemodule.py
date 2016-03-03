#!/usr/bin/env python
"""OmicsPipe API application.
   generatemodule.py get -r <pipelinerecipesid> -s <stepsid> -f <userfilesid> -o <resultfilename> -t <apitoken> > <custom_module_name>.py

Usage:
  generatemodule.py get -r <pipelinerecipesid> -s <stepsid> -f <userfilesid> -o <resultfilename> -t <apitoken>
  generatemodule.py (-h | --help)
  generatemodule.py (-v | --version)

Options:
  -r --pipelinerecipesid <pipelinerecipesid> input pipelinerecipe id
  -s --stepsid <stepsid> input stepid id
  -f --userfilesid <userfilesid> show userfile id
  -o --resultfilename <resultfilename> input resultfile name that inclued file type
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

url_steps = 'http://aws1niagads.org:8000/steps/' + arguments['--stepsid'] #31
url_userfiles = 'http://aws1niagads.org:8000/userfiles/' + arguments['--userfilesid'] #3
url_modules = 'http://aws1niagads.org:8000/modules/'
url_pipelinerecipes = 'http://aws1niagads.org:8000/pipelinerecipes/' + arguments['--pipelinerecipesid'] #2
token = arguments['--apitoken']
headers = {'Authorization': '%s' % token}
request_steps = Request(url_steps, headers=headers)
request_userfiles = Request(url_userfiles, headers=headers)
request_modules = Request(url_modules, headers=headers)
request_pipelinerecipes = Request(url_pipelinerecipes, headers=headers)
response_steps = urlopen(request_steps)
response_userfiles = urlopen(request_userfiles)
response_modules = urlopen(request_modules)
response_pipelinerecipes = urlopen(request_pipelinerecipes)
data_steps = json.loads(response_steps.read())
data_userfiles = json.loads(response_userfiles.read())
data_modules = json.loads(response_modules.read())
data_pipelinerecipes = json.loads(response_pipelinerecipes.read())
step_list = []


def  originalEnv():
    print "#!/usr/bin/env python"
    print "from omics_pipe.parameters.default_parameters import default_parameters"
    print "from omics_pipe.utils import *"
    print "p = Bunch(default_parameters)"

def  originalModule(data_steps, data_userfiles, data_modules, url_modules, data_pipelinerecipes, token, headers):
    #print data_steps['modules']
    print "def " + data_steps['title'] + "(sample," + data_steps['title'] + "_flag):"
    for num in data_modules:
       if str(num['name']) == data_steps['title']:
           #print str(num['id'])
           url_moduleid = url_modules + str(num['id'])
           request_moduleid = Request(url_moduleid, headers=headers)
           response_moduleid = urlopen(request_moduleid)
           data_module = json.loads(response_moduleid.read())
           print "    '''" + data_module['description']
           print "    input:"
           print "         " + data_module['inputformat']
           print "    output:"
           print "          " + data_module['outputformat']
           print "    citation:"
           print "          " + data_module['softwarecitation']
           print "    link:"
           print "          " + data_module['softwarelink']
           print "    parameters from parameters file:"
           print "          " + data_module['parameters']
           print "    '''"

           parameters = re.sub("[\s]", 'p.', str(data_module['parameters']))
           print "    spawn_job(jobname = '" + data_steps['title'] + "', SAMPLE = sample, LOG_PATH = p.LOG_PATH, RESULTS_EMAIL = p.RESULTS_EMAIL, SCHEDULER = p.SCHEDULER, walltime = '" + data_module['time'] + "', queue = p.QUEUE, nodes = 1, ppn = 4, memory = '" + data_module['memory'] + "', script = '" + data_userfiles['path'] + "', args_list = [p." + parameters + "])"
           print "    job_status(jobname = '" + data_module['name'] + "', resultspath = p.BWA_RESULTS, SAMPLE = sample, outputfilename = " + data_pipelinerecipes['resultpath'] + "/"+ arguments['--resultfilename'] + ", FLAG_PATH = p.FLAG_PATH)"
           print "    return"

           print "if __name__ == '__main__':"
           print "    " + data_steps['title'] + "(sample," + data_steps['title'] + "_flag)"
           print "    sys.exit(0)"

originalEnv()
originalModule(data_steps, data_userfiles, data_modules, url_modules, data_pipelinerecipes, token, headers)
