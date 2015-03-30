from setuptools import setup, find_packages

setup(
  name = 'recast-dev-server',
  version = '0.0.1',
  description = 'server that ca be used to develop new recastable analyses',
  long_description = 'this is  a stub server that can be used to develop the result blueprints for recast analyses',
  url = 'http://example.com',
  author = 'Lukas Heinrich',
  author_email = 'lukas.heinrich@cern.ch',
  packages=find_packages(),
  entry_points={
        'console_scripts': ['recast-devserver = recastdevserver.server:runserver']
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