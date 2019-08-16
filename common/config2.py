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
        # iterate through the service's configs and audit the schema itself:
        for c in schema:
            name = c.get('name')
            if not name:
                msg = f"Invalid service config schema; property 'name' missing from config {c}."
                raise errors.ServiceConfigError(msg=msg)
            typ = c.get("typ")
            if not typ:
                msg = f"Invalid service config schema; property 'typ' missing from config {c}."
                raise errors.ServiceConfigError(msg=msg)
            try:
                required = c["required"]
            except KeyError:
                msg = f"Invalid service config schema; property 'required' missing from config {c}."
                raise errors.ServiceConfigError(msg=msg)
            if not typ:
                msg = f"Invalid service config schema; property 'typ' missing from config {c}."
                raise errors.ServiceConfigError(msg=msg)
            # optional fields -
            default = c.get('default')
            if not type(default) == typ:
                msg = f"Invalid service config schema; invalid type for property 'default'. " \
                      f"The required type is {typ} but the object given was type {type(default)}. config: {c}."
                raise errors.ServiceConfigError(msg=msg)
            desc = c.get('description', '')
            values = c.get('values')

            # check the base schema for this attribute; any configs specified in the service schmea override those
            # in the base.
            found = False
            for b in result:
                if b['name'] == name:
                    found = True
                    b['typ'] = typ
                    b['required'] = required
                    b['default'] = default
                    b['desc'] = desc
                    break
            # if we didn't find a config in the base, apppend it to the result
            if not found:
                result.append({...})


    def __init__(self):
        """
        
        """
        self.schema = self.get_config_schema()

service_config = Config()
