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
        'console_scripts': ['recast-devserver = recastdevkit.devserver.server:runserver']
      },
  include_package_data=True,
  zip_safe=False,
  install_requires = [
    'Flask',
    'gevent',
    'gevent-socketio',
  ],
  dependency_links = [
  ]
)