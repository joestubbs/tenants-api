from flask_restful import Resource
# from flasgger import swag_from
from common import utils
from models import LDAPConnection

class LDAPsResource(Resource):
    """
    Work with LDAP connection objects
    """

    # @swag_from("resources/ldaps/list.yml")
    def get(self):
        ldaps = LDAPConnection.query.all()
        return utils.ok(result=ldaps, msg="LDAPs retrieved successfully.")

    def post(self):
        pass

