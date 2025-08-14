

class OWMException(Exception):
    """Base exception for OWM service errors."""

class OWMAPIException(OWMException):
    """HTTP related OWM API errors."""
    def __init__(self, message: str, status_code=None, original_exception=None):
        super().__init__(message)
        self.status_code = status_code
        self.original_exception = original_exception
    

class OWMDataValidationException(OWMException):
    """Data validation errors."""
    pass


class OWMDataException(OWMException):
    """Data parsing/formatting errors."""
    pass






