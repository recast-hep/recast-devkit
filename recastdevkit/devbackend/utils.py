import recastbackend.backendtasks  
import recastdevkit.devbackend.devtasks
import recastbackend.utils
import uuid

def postchain(request_uuid,point,queuename,resultlist,backend):           
  post = ( recastdevkit.devbackend.devtasks.postresults.subtask((request_uuid,point,resultlist,backend),queue=queuename) )
  return post

def wrapped_chain(request_uuid,point,analysis_chain,resultlist,queuename,backend):
  jobguid = uuid.uuid1()
  
  pre  =  recastbackend.utils.prechain(request_uuid,point,jobguid,queuename)
  post =  postchain(request_uuid,point,queuename,resultlist,backend)

  chain = (pre | analysis_chain | post)
  return (jobguid,chain)
