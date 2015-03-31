import click
import recastdevkit.devbackend.utils
from recastbackend.submitter import agnostic_submit
from recastdevkit.devbackend.localapp import app

@click.command()
@click.argument('uuid')
@click.argument('parameter')
@click.argument('queue')
@click.argument('modulename')
def submit(uuid,parameter,queue,modulename):
    return agnostic_submit(uuid,parameter,recastdevkit.devbackend.utils.wrapped_chain,queue,modulename)