# recast-dev-server
development server for RECAST for analysis plugin development

to start the server use the recast-devserver entry point and provide as arguments the blueprint module and the working directory from which to pull result files

    recast-devserver <blueprint import string, e.g.: recasthelloworld.blueprint> <workdir path, e.g. /path/to/workdir>

to start the development backend celery instance to something like

    celery worker -A recastdevkit.devbackend.localapp:app -I recasthelloworld.backendtasks,recastbackend.backendtasks,recastdevkit.devbackend.devtasks -l info -Q hello_world_queue
