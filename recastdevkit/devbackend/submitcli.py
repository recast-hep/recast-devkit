import click
import recastdevkit.devbackend.utils
import importlib
from recastbackend.submission import agnostic_celery_submit
from recastbackend.submitter import wait_and_echo

from recastdevkit.devbackend.localapp import app


def development_dedicated_celery_submit(uuid,parameter,modulename):
  queue = 'celery'
  module = importlib.import_module(modulename)
  resultlist = module.resultlist
  analysis_chain = module.get_chain(queue)
  
  return agnostic_celery_submit(uuid, parameter, queue, analysis_chain, resultlist,
                                recastdevkit.devbackend.utils.wrapped_chain,'dedicated')


def development_rivet_celery_submit(uuid,parameter,analysis):
  queue = 'celery'
  module = importlib.import_module('recastrivet.backendtasks')
  resultlist = module.resultlist
  analysis_chain = module.get_chain(queue,analysis)
  
  return agnostic_celery_submit(uuid, parameter, queue, analysis_chain, resultlist,
                                recastdevkit.devbackend.utils.wrapped_chain,'rivet')


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
