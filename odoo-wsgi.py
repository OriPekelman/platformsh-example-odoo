# WSGI Handler sample configuration file.
#
# Change the appropriate settings below, in order to provide the parameters
# that would normally be passed in the command-line.
# (at least conf['addons_path'])
#
# For generic wsgi handlers a global application is defined.
# For uwsgi this should work:
#   $ uwsgi_python --http :9090 --pythonpath . --wsgi-file openerp-wsgi.py
#
# For gunicorn additional globals need to be defined in the Gunicorn section.
# Then the following command should run:
#   $ gunicorn odoo:service.wsgi_server.application -c openerp-wsgi.py

import odoo
import base64
import json
import os
#----------------------------------------------------------
# Common
#----------------------------------------------------------
odoo.multi_process = True # Nah!

# Equivalent of --load command-line option
odoo.conf.server_wide_modules = ['web']
conf = odoo.tools.config

# Path to the OpenERP Addons repository (comma-separated for
# multiple locations)

conf['addons_path'] = './addons/'

# Optional database config if not using local socket

relationships = os.getenv('PLATFORM_RELATIONSHIPS')
if relationships:
    relationships = json.loads(base64.b64decode(relationships).decode('utf-8'))
    db_settings = relationships['database'][0]
    conf['db_name'] = db_settings['path']
    conf['db_host'] = db_settings['host']
    conf['db_user'] = db_settings['username']
    conf['db_port'] = db_settings['port']
    conf['db_password'] = db_settings['password']

#----------------------------------------------------------
# Generic WSGI handlers application
#----------------------------------------------------------
application = odoo.service.wsgi_server.application

odoo.service.server.load_server_wide_modules()

##----------------------------------------------------------
## Gunicorn
##----------------------------------------------------------
## Standard OpenERP XML-RPC port is 8069
#bind = '127.0.0.1:8069'
xmlrpc_port=os.getenv('PORT')
#pidfile = '.gunicorn.pid'
#workers = 4
#timeout = 240
#max_requests = 2000
#