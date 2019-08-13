"""
Base configuration schema for any Tapis flask API.

The schema object is a Python list of dictionaries, with each dictionary correspoding to a single configuration for 
the service. The follwing atributes are available:

* name (str) - the name of the config attribute.
* typ (Python type) - the type of the value config attribute.
* required (bool) - whether the attribute is required.
* description (str) - A description of the configuration.
* default (typ) - (optional) - the defualt value for the config when no config is specified. 
* values ([typ]) - (optional) - A list of allowable values for the config.

"""

from common import api

base_schema = [
    {
        "name": "server",
        "typ": str,
        "required": False,
        "description": "configures whether to run the development server or the production server.",
        "default": "dev",
        "values": ["dev", "prod"]
    },
    {
        "name": "log_level",
        "typ": str,
        "required": False,
        "default": "DEBUG",
        "description": "the logging level to use for the service. ",
        "values": ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]
    },
    {
        "name": "log_file",
        "typ": str,
        "required": False,
        "description": "location of log file.",
        "default": f"/home/tapis/{api}/{api}.log",
    },


]