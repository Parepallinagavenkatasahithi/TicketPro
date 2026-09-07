from fastapi import HTTPException, status


class TicketProException(HTTPException):
    def __init__(self, status_code: int, detail: str, code: str = "ERROR"):
        super().__init__(status_code=status_code, detail=detail)
        self.code = code


class AuthenticationError(TicketProException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            code="AUTHENTICATION_FAILED"
        )


class PermissionDeniedError(TicketProException):
    def __init__(self, detail: str = "Permission denied for this operation"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            code="PERMISSION_DENIED"
        )


class NotFoundError(TicketProException):
    def __init__(self, resource: str = "Resource", identifier: str = ""):
        detail = f"{resource} not found" if not identifier else f"{resource} '{identifier}' not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            code="NOT_FOUND"
        )


class InvalidStateTransitionError(TicketProException):
    def __init__(self, from_state: str, to_state: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot transition ticket state from '{from_state}' to '{to_state}'",
            code="INVALID_STATE_TRANSITION"
        )


class ValidationError(TicketProException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            code="VALIDATION_ERROR"
        )


class AttachmentError(TicketProException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            code="ATTACHMENT_ERROR"
        )


class SLAError(TicketProException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            code="SLA_ERROR"
        )


class ApprovalError(TicketProException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            code="APPROVAL_ERROR"
        )
