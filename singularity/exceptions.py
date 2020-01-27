class APIException(Exception):
    """An exception for API errors."""


class GatewayTimeoutException(APIException):
    """An exception for 504 errors."""

