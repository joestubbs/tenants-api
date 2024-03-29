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
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    institution = db.Column(db.String(80), unique=True, nullable=False)
    # tenants = db.relationship("Tenant", backref="owner")

    def __repr__(self):
        return f'{self.username}, {self.institution}'

    @property
    def serialize(self):
        return {
            "email": self.email,
            "name": self.name,
            "institution": self.institution,
        }


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
    ldap_id = db.Column(db.String(50), unique=True, nullable=False)
    url = db.Column(db.String(2000), unique=False, nullable=False)
    user_dn = db.Column(db.String(200), unique=False, nullable=False)
    bind_dn = db.Column(db.String(200), unique=False, nullable=False)
    bind_credential = db.Column(db.String(200), unique=False, nullable=False)
    account_type = db.Column(db.Enum(LDAPAccountTypes), unique=False, nullable=False)

    @property
    def serialize(self):
        return {
            'ldap_id': self.ldap_id,
            'url': self.url,
            'user_dn': self.user_dn,
            'bind_dn': self.bind_dn,
            'bind_credential': self.bind_credential,
            'account_type': self.account_type.serialize,
        }


class Tenant(db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.String(50), unique=True, nullable=False)
    base_url = db.Column(db.String(2000), unique=True, nullable=False)
    token_service = db.Column(db.String(2000), unique=True, nullable=False)
    security_kernel = db.Column(db.String(2000), unique=True, nullable=False)
    owner = db.Column(db.String(120), db.ForeignKey('tenantOwners.email'), nullable=False)
    # ldap connections are not required if the tenant will use an alternative mechanism for authenticating accounts -
    service_ldap_connection_id = db.Column(db.String(50), db.ForeignKey('ldap_connections.ldap_id'), nullable=True)
    user_ldap_connection_id = db.Column(db.String(50), db.ForeignKey('ldap_connections.ldap_id'), nullable=True)
    description = db.Column(db.String(1000), unique=False, nullable=True)

    def __repr__(self):
        return f'{self.tenant_id}: {self.description}'

    @property
    def serialize(self):
        return {
            'tenant_id': self.tenant_id,
            'base_url': self.base_url,
            'token_service': self.token_service,
            'security_kernel': self.security_kernel,
            'owner': self.owner,
            'service_ldap_connection_id': self.service_ldap_connection_id,
            'user_ldap_connection_id': self.user_ldap_connection_id,
            'description': self.description,
        }