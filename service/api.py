from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand

from common.config import conf
from common.utils import TapisApi, handle_error

from controllers import LDAPsResource
from errors import errors
from models import db, app

# db and migrations ----
db.init_app(app)
migrate = Migrate(app, db)

# connexion -----
# db.init_app(app.app)
# migrate = Migrate(app.app, db)
#
# app.add_api('openapi_v3.yml')


# flasgger ----
# from flasgger import Swagger
# app.config['SWAGGER'] = {
#     'title': 'Tenants',
#     'openapi': '3.0.2'
# }
# Swagger(app)

# flask restful API object ----
api = TapisApi(app, errors=errors)

# Set up error handling
api.handle_error = handle_error
api.handle_exception = handle_error
api.handle_user_exception = handle_error

# Add resources
api.add_resource(LDAPsResource, '/ldaps')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)