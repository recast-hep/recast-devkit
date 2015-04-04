import click
import importlib
import recastbackend.backendtasks
import recastdevkit.devbackend.devtasks

from recastbackend.submitter import wait_and_echo
from recastdevkit.devbackend.localapp import app
from recastbackend.backendtasks import run_analysis

def development_dedicated_celery_submit(uuid,parameter,modulename):
  queue = 'celery'
  jobguid = '0.0.0.0'
  app.set_current()

  ctx = dict(
      jobguid       = jobguid,
      requestguid   = uuid,
      parameter_pt  = parameter,
      entry_point   = '{}:recast'.format(modulename),
      results       = '{}:resultlist'.format(modulename),
      backend       = 'dedicated'
  )

  result =  run_analysis.apply_async((recastbackend.backendtasks.setup,
                                      recastdevkit.devbackend.devtasks.onsuccess,
                                      recastbackend.backendtasks.cleanup,ctx),
                                      queue = queue)
  return (jobguid,result)
  

def development_rivet_celery_submit(uuid,parameter,analysis):
  queue = 'celery'
  jobguid = '0.0.0.0'
  app.set_current()

  ctx = dict(
      jobguid       = jobguid,
      requestguid   = uuid,
      parameter_pt  = parameter,
      entry_point   = '{}:recast'.format('recastrivet.backendtasks'),
      results       = '{}:resultlist'.format('recastrivet.backendtasks'),
      backend       = 'rivet',
      analysis      = analysis
  )

  result =  run_analysis.apply_async((recastbackend.backendtasks.setup,
                                      recastdevkit.devbackend.devtasks.onsuccess,
                                      recastbackend.backendtasks.cleanup,ctx),
                                      queue = queue)

  return (jobguid,result)


@click.group()
def cli():
  pass
  
@cli.command()
@click.argument('uuid')
@click.argument('parameter')
@click.argument('modulename')
def dedicated(uuid,parameter,modulename):
    jobguid,result =  development_dedicated_celery_submit(uuid,parameter,modulename)    
    return wait_and_echo(result)


@cli.command()
@click.argument('uuid')
@click.argument('parameter')
@click.argument('analysis')
def rivet(uuid,parameter,analysis):
    jobguid,result =  development_rivet_celery_submit(uuid,parameter,analysis)
    return wait_and_echo(result)
