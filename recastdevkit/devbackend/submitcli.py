import click
import recastdevkit.devbackend.devtasks
import redis
import msgpack
import celery
import time

def get_parents(child):
  x = child.parent
  while x:
    yield x
    x = x.parent

def pubsub_or_ready(result,pubsub):
  while True:
    message = pubsub.get_message()
    # if our result is ready (failed or successful)
    # or one of the parents failed we're done
    if result.ready() or any(map(lambda x:x.failed(),get_parents(result))):
      return
    if message:
      yield message      
    time.sleep(0.001)  # be nice to the system :)    

@click.command()
@click.argument('uuid')
@click.argument('parameter')
@click.argument('queue')
@click.argument('modulename')
def submit(uuid,parameter,queue,modulename):
  from recastdevkit.devbackend.localapp import app
  j,c = recastdevkit.devbackend.devtasks.wrapped_chain(uuid,parameter,queue,modulename)
  result = c.apply_async()
  click.secho('submitted chain for module {}'.format(modulename))
  
  
  red = redis.StrictRedis(host = celery.current_app.conf['CELERY_REDIS_HOST'],
                            db = celery.current_app.conf['CELERY_REDIS_DB'], 
                          port = celery.current_app.conf['CELERY_REDIS_PORT'])
  pubsub = red.pubsub()
  pubsub.subscribe('socket.io#emitter')
  for m in pubsub_or_ready(result,pubsub):
    if m['type'] == 'message':
      data =  msgpack.unpackb(m['data'])[0]
      extras =  msgpack.unpackb(m['data'])[1]
      if(data['nsp'] == '/monitor'):
        click.secho('received message: {date} -- {msg}'.format(**(data['data'][1])),fg = 'blue')
  if result.successful():
    click.secho('chain suceeded',fg = 'green')
  else:
    click.secho('chain failed somewhere',fg = 'red')
    