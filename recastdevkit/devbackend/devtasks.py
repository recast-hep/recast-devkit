import os
import shutil
import importlib
import logging

from recastbackend.backendtasks import isolate_results
log = logging.getLogger('RECAST')

def onsuccess(ctx):
  DUMMYRESULTDIR = os.environ['RECAST_DUMMYRESULTDIR']
  assert DUMMYRESULTDIR
  
  log.info('dev version of onsuccess. copying into: {}'.format(DUMMYRESULTDIR))

  jobguid = ctx['jobguid']
  resultlistname = ctx['results']
  backend = ctx['backend']

  modulename,attr = resultlistname.split(':')
  module = importlib.import_module(modulename)
  resultlister = getattr(module,attr)
  
  resultdir = isolate_results(jobguid,resultlister())


  dedicated_dir = '{}/{}'.format(DUMMYRESULTDIR,backend)
  if(os.path.exists(dedicated_dir)):
    shutil.rmtree(dedicated_dir)

  shutil.copytree(resultdir, dedicated_dir)

  log.info('done copying results')
