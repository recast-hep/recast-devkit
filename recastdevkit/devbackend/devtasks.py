from celery import task
import os
import shutil
import recastbackend.backendtasks  
import uuid
import importlib


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


def postchain(request_uuid,point,queuename,resultlist):           
  post = ( postresults.subtask((request_uuid,point,resultlist),queue=queuename) )
  return post

def wrapped_chain(request_uuid,point,queuename,modulename):
  analysis_module = importlib.import_module(modulename)
  
  jobguid = uuid.uuid1()
  
  pre  =  recastbackend.backendtasks.prechain(request_uuid,point,jobguid,queuename)
  post =  postchain(request_uuid,point,queuename,analysis_module.resultlist)

  chain = (pre | analysis_module.get_chain(queuename) | post)
  return (jobguid,chain)
