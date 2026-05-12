from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.shared.exceptions import (
    DomainError,
    EmailAlreadyInUseError,
    InvalidCredentialsError,
    InvalidDocumentError,
    MissingConfigurationError,
    ServiceUnavailableError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvalidDocumentError)
    async def handle_invalid_document(_request: Request, exc: InvalidDocumentError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(MissingConfigurationError)
    async def handle_missing_configuration(
        _request: Request, exc: MissingConfigurationError
    ) -> JSONResponse:
        return JSONResponse(status_code=500, content={"detail": str(exc)})

    @app.exception_handler(ServiceUnavailableError)
    async def handle_service_unavailable(
        _request: Request, exc: ServiceUnavailableError
    ) -> JSONResponse:
        return JSONResponse(status_code=503, content={"detail": str(exc)})

    @app.exception_handler(EmailAlreadyInUseError)
    async def handle_email_in_use(_request: Request, exc: EmailAlreadyInUseError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(InvalidCredentialsError)
    async def handle_invalid_credentials(
        _request: Request, exc: InvalidCredentialsError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(DomainError)
    async def handle_domain_error(_request: Request, exc: DomainError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})
