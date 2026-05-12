class DomainError(Exception):
    """Base exception for application errors."""


class InvalidDocumentError(DomainError):
    """Raised when a document cannot be parsed or indexed."""


class MissingConfigurationError(DomainError):
    """Raised when required runtime configuration is missing."""


class ServiceUnavailableError(DomainError):
    """Raised when an external dependency is unavailable."""


class EmailAlreadyInUseError(DomainError):
    """Raised when registering with an e-mail that already exists."""


class InvalidCredentialsError(DomainError):
    """Raised when login credentials are wrong."""
