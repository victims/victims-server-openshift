#!/usr/bin/python
import os
import sys

PY_VERSION = '%d.%d' % (sys.version_info[0], sys.version_info[1])
PY_DIR = 'python-%s' % (PY_VERSION)

# source: https://github.com/openshift/flask-example
sys.path.insert(0, os.path.dirname(__file__) or '.')

# add libs
sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'libs'))

if os.path.exists(os.path.join(os.environ['OPENSHIFT_HOMEDIR'], PY_DIR)):
    PY_DIR = os.path.join(os.environ['OPENSHIFT_HOMEDIR'], PY_DIR)
else:
    PY_DIR = os.path.join(os.environ['OPENSHIFT_HOMEDIR'], 'python')

virtenv = PY_DIR + '/virtenv/'

PY_CACHE = os.path.join(virtenv, 'lib', PY_VERSION, 'site-packages')

os.environ['PYTHON_EGG_CACHE'] = os.path.join(PY_CACHE)
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')

try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass

# Instance configurations
DB_NAME = os.environ['OPENSHIFT_APP_NAME']
if len(DB_NAME.strip()) == 0:
    DB_NAME = 'victimsweb'
os.environ['VICTIMS_DB_NAME'] = DB_NAME
config_file = os.path.join(
    os.environ['OPENSHIFT_DATA_DIR'], 'victimsweb.cfg')
if not os.path.exists(config_file):
    config_file = os.path.join(
        os.environ['OPENSHIFT_REPO_DIR'], 'config', 'victimsweb.cfg')
os.environ['VICTIMS_CONFIG'] = config_file
os.environ['VICTIMS_LOG_DIR'] = os.environ['OPENSHIFT_PYTHON_LOG_DIR']

# Start the application
from victims_web.application import app as application
application.run(host=os.environ['OPENSHIFT_PYTHON_IP'],
                port=int(os.environ['OPENSHIFT_PYTHON_PORT']))
