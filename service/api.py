from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand

# from .controllers import TenantsResource
from .models import db

app = Flask(__name__)

from common.config import conf

app.config['SQLALCHEMY_DATABASE_URI'] = conf.sql_db_url
db.init_app(app)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)