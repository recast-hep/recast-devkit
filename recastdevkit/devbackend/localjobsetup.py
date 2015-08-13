import os
import zipfile
import logging
import urllib2
import StringIO

log = logging.getLogger('RECAST')

def prepare_workdir(jobguid):
  workdir = 'workdirs/{}'.format(jobguid)
  os.makedirs(workdir)
  log.info('prepared workdir {}'.format(workdir))
  return workdir

def prepare_job(workdir,filepath):
  with zipfile.ZipFile(StringIO.StringIO(urllib2.urlopen(filepath).read()))as f:
    f.extractall('{}/inputs'.format(workdir)) 

def setup(ctx):
  log.info('setting up job for context {}'.format(ctx))

  workdir = prepare_workdir(ctx['jobguid'])
  prepare_job(workdir,ctx['filepath'])
