import enum
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from common.config import conf
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = conf.sql_db_url
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# import connexion
# app = connexion.FlaskApp(__name__, specification_dir='resources/')
# app.app.config['SQLALCHEMY_DATABASE_URI'] = conf.sql_db_url
# db = SQLAlchemy(app.app)
# migrate = Migrate(app.app, db)


class TenantOwner(db.Model):
    __tablename__ = 'tenantOwners'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    institution = db.Column(db.String(80), unique=True, nullable=False)
    tenants = db.relationship("Tenant", backref="owner")

    def __repr__(self):
        return f'{self.username}, {self.institution}'


class LDAPAccountTypes(enum.Enum):
    user = 'user'
    service = 'service'

    def __repr__(self):
        if self.user:
            return 'user'
        return 'service'

    @property
    def serialize(self):
        return str(self)


class LDAPConnection(db.Model):
    __tablename__ = 'ldap_connections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2000), unique=True, nullable=False)
    url = db.Column(db.String(2000), unique=False, nullable=False)
    user_dn = db.Column(db.String(200), unique=False, nullable=False)
    bind_dn = db.Column(db.String(200), unique=False, nullable=False)
    bind_credential = db.Column(db.String(200), unique=False, nullable=False)
    account_type = db.Column(db.Enum(LDAPAccountTypes), unique=False, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'bind_dn': self.bind_dn,
            'bind_credential': self.bind_credential,
            'account_type': self.account_type.serialize,
        }


class Tenant(db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.String(80), unique=True, nullable=False)
    base_url = db.Column(db.String(2000), unique=True, nullable=False)
    token_service = db.Column(db.String(2000), unique=True, nullable=False)
    security_kernel = db.Column(db.String(2000), unique=True, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('tenantOwners.id'), nullable=False)
    service_ldap_connection_id = db.Column(db.Integer, db.ForeignKey('ldap_connections.id'), nullable=False)
    user_ldap_connection_id = db.Column(db.Integer, db.ForeignKey('ldap_connections.id'), nullable=False)

    def __repr__(self):
        return f'{self.tenant_id}: {self.description}'