from setuptools import setup, find_packages

setup(
  name = 'recast-devkit',
  version = '0.0.1',
  description = 'development kit for recast',
  long_description = 'set of packages and applications to help develop recast analysis plugins',
  url = 'http://example.com',
  author = 'Lukas Heinrich',
  author_email = 'lukas.heinrich@cern.ch',
  packages=find_packages(),
  entry_points={
        'console_scripts': ['recast-devserver = recastdevkit.devserver.server:runserver',
                            'recast-devsub = recastdevkit.devbackend.submitcli:cli']
      },
  include_package_data=True,
  zip_safe=False,
  install_requires = [
    'Flask',
    'gevent',
    'gevent-socketio',
    'recast-backend',
    'socket.io-emitter',
    'click'
    
  ],
  dependency_links = [
    'https://github.com/ziyasal/socket.io-python-emitter/tarball/master#egg=socket.io-emitter-0.1.3',
    'https://github.com/recast-hep/recast-backend/tarball/master#egg=recast-backend-0.0.1'
  ]
)
