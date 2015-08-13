import click
import importlib
import recastbackend.backendtasks
import recastdevkit.devbackend.devtasks
import recastdevkit.devbackend.localjobsetup

from recastbackend.submitter import wait_and_echo
from recastdevkit.devbackend.localapp import app
from recastbackend.backendtasks import run_analysis

@click.group()
def cli():
  pass
  
@cli.command()
@click.argument('modulename')
@click.argument('filepath')
def dedicated(modulename,filepath):
    ctx = {'jobguid':'jobguid',
           'filepath':filepath,
           'entry_point':'{}:recast'.format(modulename),
           'results':'{}:resultlist'.format(modulename),
           'backend':'dedicated'}


    result = run_analysis.apply_async((recastdevkit.devbackend.localjobsetup.setup,
			               recastdevkit.devbackend.devtasks.onsuccess,
                                       recastbackend.backendtasks.cleanup,
                                       ctx))

    return wait_and_echo(result)
