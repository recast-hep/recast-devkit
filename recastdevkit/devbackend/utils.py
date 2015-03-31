import recastbackend.backendtasks  
import recastdevkit.devbackend.devtasks
import uuid

def postchain(request_uuid,point,queuename,resultlist):           
  post = ( recastdevkit.devbackend.devtasks.postresults.subtask((request_uuid,point,resultlist),queue=queuename) )
  return post

def wrapped_chain(request_uuid,point,analysis_chain,resultlist,queuename):
  jobguid = uuid.uuid1()
  
  pre  =  recastbackend.backendtasks.prechain(request_uuid,point,jobguid,queuename)
  post =  postchain(request_uuid,point,queuename,resultlist)

  chain = (pre | analysis_chain | post)
  return (jobguid,chain)
