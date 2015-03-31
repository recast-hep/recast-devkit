from celery import task
import os
import shutil

@task
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


  DUMMYRESULT_DIR = os.environ['RECAST_DUMMYWORKDIR']
  assert DUMMYRESULT_DIR
  if(os.path.exists(DUMMYRESULT_DIR)):
    shutil.rmtree(DUMMYRESULT_DIR)

  shutil.copytree(resultdir, DUMMYRESULT_DIR)

  return requestId
