import click
import subprocess
import os

@click.command()
@click.argument('backendmodule')
@click.argument('resultdir')
def startcelery(backendmodule,resultdir):
  env = os.environ
  env['RECAST_DUMMYRESULTDIR'] = os.path.abspath(resultdir)
  subprocess.Popen(['redis-server'])
  subprocess.call(['celery','worker','-A','recastdevkit.devbackend.localapp','-l','info'], env = env)