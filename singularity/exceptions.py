class APIException(Exception):
    """An exception for API errors."""
    def __init__(self, error_code, error_detail, status_code=None):
        """Create a new error

        :param error_code str: the ID code for the error
        :param error_detail str: detailed information about the error
        :param status_code int: (default: None) the status code of the response
        """
        self.error_code = error_code
        self.error_detail = error_detail
        if status_code is not None:
            self.status_code = status_code
        else:
            self.status_code = 400

    def __repr__(self):
        code = self.error_code
        if self.error_code is None:
            code = 'no-error-code'

        detail = self.error_detail
        if self.error_detail is None:
            detail = 'no detail about the error was provided'

        status = self.status_code

        return "<APIException[{}] ({}: {})>".format(status, code, detail)



class GatewayTimeoutException(APIException):
    """An exception for 504 errors."""

