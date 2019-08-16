"""
Validates service configuration based on jsonschema for any Tapis flask API. The base schema for all services is
configschema.json, in this repo, but services can update or override the schema definition with

"""
import json
import jsonschema
import os

from errors import BaseTapisError

# load the base api schema -
schema = json.load(open('configschema.json', 'r'))

# try to load an api-specific schema
service_configschema_path = os.environ.get('TAPIS_CONFIGSCHEMA_PATH', '/home/tapis/configschema.json')
try:
    api_schema = json.load(open(service_configschema_path, 'r'))
except Exception as e:
    # at this point, logging is not set up yet, so we just print the message to the screen and hope for the best:
    msg = f'ERROR, improperly configured service. Could not load configschema.json found; ' \
          f'looked in {service_configschema_path}. Aborting. Exception: {e}'
    print(msg)
    raise BaseTapisError(msg)

# we override properties defined in the base schema with properties defined in the service schema
api_properties = api_schema.get('properties')
if api_properties and type(api_properties) == dict:
    schema['properties'] = schema['properties'].update(api_properties)

# we extend the required properties with those specified as required by the API -
api_required = api_schema.get('required')
if api_required and type(api_required) == list:
    schema['required'].extend(api_required)


# now that we have the required API config schema, we need to validate it against the actual configs supplied
# to the service.

class Config(dict):
    """
    A class containing an API service's config, as a Python dictionary, with getattr and setattr defined to make
    attribute access work like a "normal" object. One should import the singleton Conf directly from this module.

    Example usage:
    ~~~~~~~~~~~~~~
    from config import conf   <-- all service configs loaded and validated against the
    conf.some_key <-- AttributeError raised if some_key (optional) config not defined
    """
    def __getattr__(self, key):
        # returning an AttributeError is important for making deepcopy work. cf.,
        # http://stackoverflow.com/questions/25977996/supporting-the-deep-copy-operation-on-a-custom-class
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, key, value):
        self[key] = value

    def get_config_from_file(self):
        """
        Reads service config from a JSON file
        :return:
        """
        path = os.environ.get('TAPIS_CONFIG_PATH', '/home/tapis/config.json')
        if os.path.exists(path):
            try:
                return json.load(open(path, 'r'))
            except Exception as e:
                msg = f'Could not load configs from JSON file at: {path}. exception: {e}'
                print(msg)
                raise BaseTapisError(msg)

    @classmethod
    def load_config(cls):
        """
        Load the config from various places, including a JSON file and environment variables.
        :return:
        """
        file_config = self.get_config_from_file()
        # validate config against schema definition
        try:
            jsonschema.validate(instance=file_config, schema=schema)
        except SchemaError as e:
            msg = f'Invalid service config: exception: {e}'
            print(msg)
            raise BaseTapisError(msg)
        return file_config

conf = Config(Config.load_config())