"""Set up the loggers for the system."""

import logging

def get_module_log_level(name: str) -> str:
    """
    Get the log level to use for this module.
    """




def get_logger(name: str) -> logging.Logger:
    """
    Returns a properly configured logger.
         name (str) should be the module name.
    """
    logger = logging.getLogger(name)
    level = get_module_log_level(name)
    logger.setLevel(level)
    handler = logging.FileHandler(get_log_file(name))
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    handler.setLevel(level)
    logger.addHandler(handler)
    logger.info("returning a logger set to level: {} for module: {}".format(level, name))
    return logger
