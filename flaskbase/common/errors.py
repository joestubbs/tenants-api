
class BaseTapisError(Exception):
    """
    Base Tapis error class. All Error types should descend from this class.
    """
    def __init__(self, msg=None, code=400):
        """
        Create a new TapisError object. 
        :param msg: (str) A helpful string
        :param code: (int) The HTTP return code that should be returned 
        """
        self.msg = msg
        self.code = code


class ServiceConfigError(BaseTapisError):
    """Error parsing service configuration."""
    def __init__(self, msg=None, code=500):
        super(ServiceConfigError, self).__init__(msg=msg, code=code)


class PermissionsError(BaseTapisError):
    """Error checking permissions or insufficient permissions needed to perform the action."""
    def __init__(self, msg=None, code=404):
        super(PermissionsError, self).__init__(msg=msg, code=code)


class DAOError(BaseTapisError):
    """General error accessing or serializing database objects."""
    def __init__(self, msg=None, code=404):
        super(DAOError, self).__init__(msg=msg, code=code)


class ResourceError(BaseTapisError):
    """General error in the API resource layer."""
    def __init__(self, msg=None, code=404):
        super(ResourceError, self).__init__(msg=msg, code=code)
