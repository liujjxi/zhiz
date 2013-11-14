import sys
sys.path.insert(0, '.')

from zhiz import app
from CURD import Database

# appfog mysql configuration

import json, os

services_json = json.loads(os.getenv("VCAP_SERVICES"))

mysql_config = services_json['mysql-5.1'][0]['credentials']

DB_CFG = {
    'user': mysql_config['username'],
    'passwd': mysql_config['password'],
    'host': mysql_config['hostname'],
    'port': mysql_config['port'],
    'db': mysql_config['name']
}

# update database configuration
app.config['DB_CFG'] = DB_CFG
app.name = 'wsgi'
application = app # !important

# Configure database again
Database.config(**app.config['DB_CFG'])


if __name__ == '__main__':
    app.run()
