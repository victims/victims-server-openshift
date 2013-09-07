#!/usr/bin/python
import os

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
