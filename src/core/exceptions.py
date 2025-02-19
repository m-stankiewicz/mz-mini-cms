class MiniCMSException(Exception):
    """Base exception for MiniCMS"""
    pass

class NotFoundException(MiniCMSException):
    """Raised when a resource is not found"""
    pass

class ValidationError(MiniCMSException):
    """Raised when validation fails"""
    pass

class DatabaseError(MiniCMSException):
    """Raised when database operation fails"""
    pass
