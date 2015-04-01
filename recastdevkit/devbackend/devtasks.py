from celery import shared_task
import os
import shutil

@shared_task
def postresults(jobguid,requestId,parameter_point,resultlister):
  workdir = 'workdirs/{}'.format(jobguid)
  resultdir = 'results/{}/{}'.format(requestId,parameter_point)
  
  if(os.path.exists(resultdir)):
    shutil.rmtree(resultdir)
    
  os.makedirs(resultdir)  

  for result,resultpath in ((r,os.path.abspath('{}/{}'.format(workdir,r))) for r in resultlister()):
    if os.path.isfile(resultpath):
      shutil.copyfile(resultpath,'{}/{}'.format(resultdir,result))
    if os.path.isdir(resultpath):
      shutil.copytree(resultpath,'{}/{}'.format(resultdir,result))


  DUMMYRESULTDIR = os.environ['RECAST_DUMMYRESULTDIR']
  assert DUMMYRESULTDIR

  dedicated_dir = '{}/dedicated'.format(DUMMYRESULTDIR)
  if(os.path.exists(dedicated_dir)):
    shutil.rmtree(dedicated_dir)

  shutil.copytree(resultdir, dedicated_dir)

  return requestId
