import os
import gevent
import importlib

from gevent import monkey; monkey.patch_all()
from flask import Flask, send_from_directory
from socketio.server import SocketIOServer, serve

import pkg_resources
templates_path = pkg_resources.resource_filename('recastdevkit.devserver','templates')
static_path = pkg_resources.resource_filename('recastdevkit.devserver','static')

app = Flask('RECAST-demo',template_folder = templates_path, static_folder = static_path)
app.debug = True
  
DUMMYWORKDIR = ''

@app.route('/resultfile/<requestId>/<parameter_pt>/<path:file>')
def plots(requestId,parameter_pt,file):
  filepath = '{}/{}'.format(DUMMYWORKDIR,file)
  return send_from_directory(os.path.dirname(filepath),os.path.basename(filepath))

import click
@click.command()
@click.argument('blueprint')
@click.argument('workdirpath', type=click.Path(exists=True))
def runserver(blueprint,workdirpath):
  global DUMMYWORKDIR
  DUMMYWORKDIR = workdirpath
  themodule = importlib.import_module(blueprint)
  app.register_blueprint(themodule.blueprint, url_prefix='/'+themodule.RECAST_ANALYSIS_ID)
  port = 8000
  host = '0.0.0.0'
  serve(app, port = port, host = host)
