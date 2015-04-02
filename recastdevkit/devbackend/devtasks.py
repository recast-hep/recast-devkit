from celery import shared_task
from recastbackend.logging import socketlog
import os
import shutil

@shared_task
def postresults(jobguid,requestId,parameter_point,resultlister,backend):
  workdir = 'workdirs/{}'.format(jobguid)
  resultdir = 'results/{}/{}'.format(requestId,parameter_point)
  
  if(os.path.exists(resultdir)):
    shutil.rmtree(resultdir)
    
  os.makedirs(resultdir)  

  for result,resultpath in ((r,os.path.abspath('{}/{}'.format(workdir,r))) for r in resultlister()):
    if os.path.isfile(resultpath):
      shutil.copyfile(resultpath,'{}/{}'.format(resultdir,result))
    elif os.path.isdir(resultpath):
      shutil.copytree(resultpath,'{}/{}'.format(resultdir,result))
    else:
      socketlog(jobguid,'result is neither file nor dir or not present: {}'.format(resultpath))
      raise IOError

  DUMMYRESULTDIR = os.environ['RECAST_DUMMYRESULTDIR']
  assert DUMMYRESULTDIR

  dedicated_dir = '{}/{}'.format(DUMMYRESULTDIR,backend)
  if(os.path.exists(dedicated_dir)):
    shutil.rmtree(dedicated_dir)

  shutil.copytree(resultdir, dedicated_dir)

  socketlog(jobguid,'done')

  return requestId
