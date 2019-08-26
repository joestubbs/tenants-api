import json
import os

from flask import request
from flask_restful import Resource
import yaml

# from flasgger import swag_from
from common import utils, errors
from service.models import db, LDAPConnection

HERE = os.path.dirname(os.path.abspath(__file__))

from openapi_core import create_spec
from openapi_core.shortcuts import RequestValidator
from openapi_core.wrappers.flask import FlaskOpenAPIRequest
spec_dict = yaml.load(open(os.path.join(HERE, 'resources', 'openapi_v3.yml'), 'r'))
spec = create_spec(spec_dict)

class LDAPsResource(Resource):
    """
    Work with LDAP connection objects
    """

    # @swag_from("resources/ldaps/list.yml")
    def get(self):
        ldaps = LDAPConnection.query.all()
        return utils.ok(result=[l.serialize for l in ldaps], msg="LDAPs retrieved successfully.")

    def post(self):
        validator = RequestValidator(spec)
        result = validator.validate(FlaskOpenAPIRequest(request))
        if result.errors:
            raise errors.ResourceError(msg=f'Invalid POST data: {result.errors}.')
        validated_params = result.parameters
        validated_body = result.body
        ldap = LDAPConnection(name=validated_body.name,
                              url=validated_body.url,
                              user_dn=validated_body.user_dn,
                              bind_dn=validated_body.bind_dn,
                              bind_credential=validated_body.bind_credential,
                              account_type=validated_body.account_type,
                              )
        db.session.add(ldap)
        db.session.commit()
        return utils.ok(result=ldap.serialize,
                        msg="LDAP object created successfully.")



