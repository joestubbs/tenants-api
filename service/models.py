from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class TenantOwner(db.Model):
    __tablename__ = 'tenantOwners'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    institution = db.Column(db.String(80), unique=True, nullable=False)
    tenants = db.relationship("Tenant", backref="owner")

    def __repr__(self):
        return f'{self.username}, {self.institution}'


class Tenant(db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.String(80), unique=True, nullable=False)
    base_url = db.Column(db.String(2000), unique=True, nullable=False)
    token_service = db.Column(db.String(2000), unique=True, nullable=False)
    security_kernel = db.Column(db.String(2000), unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('tenantOwners.id'), nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)

    def __repr__(self):
        return f'{self.tenant_id}: {self.description}'

