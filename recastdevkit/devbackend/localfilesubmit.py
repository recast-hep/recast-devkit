import click
import importlib
import recastbackend.backendtasks
import recastdevkit.devbackend.devtasks
import recastdevkit.devbackend.localjobsetup

from recastbackend.listener import wait_and_echo
from recastdevkit.devbackend.localapp import app
from recastbackend.backendtasks import run_analysis

import yaml

@click.group()
def cli():
  pass
  
@cli.command()
@click.argument('modulename')
@click.argument('filepath')
@click.option('-c','--context', help='additional context', default = None)
def dedicated(modulename,filepath,context):
    ctx = {'jobguid':'jobguid',
           'filepath':filepath,
           'entry_point':'{}:recast'.format(modulename),
           'results':'{}:resultlist'.format(modulename),
           'backend':'dedicated'}

    if context:
      ctx.update(**yaml.load(open(context)))


    result = run_analysis.apply_async((recastdevkit.devbackend.localjobsetup.setup,
			               recastdevkit.devbackend.devtasks.onsuccess,
                                       recastbackend.backendtasks.cleanup,
                                       ctx))

    return wait_and_echo(result)
