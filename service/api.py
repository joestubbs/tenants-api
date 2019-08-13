import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from controllers import TenantsResource

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('_tapis_postgres_uri', '"postgresql://postgres/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)