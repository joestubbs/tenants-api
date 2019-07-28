"""
Parse configs from environment variables based on the config-schema for the service and the base Tapis flask service
config.
"""
from common import api
from common import errors
from configschema import base_schema
from service.configs import schema

class Config(object):

    def get_config_schema(self):
        """
        Get the config schema for the current API service. This
        :return: [dict]
        """
        result = base_schema
        # iterate through the service's configs; any configs specified in the service schmea override those
        # in the base
        for c in schema:
            name = c.get('name')
            if not name:
                msg = f"Invalid service config schema; property 'name' missing from config {c}."
                raise errors.ServiceConfigError(msg=msg)
            typ = c.get("typ")
            if not typ:
                msg = f"Invalid service config schema; property 'typ' missing from config {c}."
                raise errors.ServiceConfigError(msg=msg)


    def __init__(self):
        """
        
        """
        self.schema = self.get_config_schema()

service_config = Config()
