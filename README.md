# recast-dev-server
development server for RECAST for analysis plugin development

to start the server use the recast-devserver entry point and provide as arguments the blueprint module and the working directory from which to pull result files

    recast-devserver <blueprint import string, e.g.: recasthelloworld.blueprint> <workdir path, e.g. /path/to/workdir>

to start the development backend celery instance to something like

    RECAST_DUMMYWORKDIR=$PWD/dummy_workdir celery worker -A recastdevkit.devbackend.localapp:app -I recasthelloworld.backendtasks,recastbackend.backendtasks,recastdevkit.devbackend.devtasks -l info -Q hello_world_queue

to submit the analysis chain to something like
    
    recast-devsub c53a29c7-2fef-6004-d1f2-4e5567af5cc5 parameter-0 hello_world_queue recasthelloworld.backendtasks
