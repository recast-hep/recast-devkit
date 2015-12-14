Build

# recast-devkit

mini development kit for developing RECAST plugins

to start the server use the recast-devserver entry point and provide as arguments the blueprint module and the working directory from which to pull result files

    recast-devserver <blueprint import string, e.g.: recasthelloworld.blueprint> <resultdir path>

to start the development backend celery instance to something like (make sure you have a redis instance running)

    recast-devbackend <backendtasks import string, e.g.: recasthelloworld.backendtasks> <resultdir path>

to submit the analysis chain to something like
    
    recast-devsub c53a29c7-2fef-6004-d1f2-4e5567af5cc5 parameter-0 hello_world_queue recasthelloworld.backendtasks

instead of starting all processes independently in separate shells you can also install honcho and prepare a Procfile.
