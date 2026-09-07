from typing import Dict, Set
from app.models.ticket import TicketStatus
from app.core.exceptions import InvalidStateTransitionError

VALID_TRANSITIONS: Dict[TicketStatus, Set[TicketStatus]] = {
    TicketStatus.NEW: {
        TicketStatus.OPEN,
        TicketStatus.ASSIGNED,
        TicketStatus.CANCELLED
    },
    TicketStatus.OPEN: {
        TicketStatus.ASSIGNED,
        TicketStatus.IN_PROGRESS,
        TicketStatus.WAITING_FOR_USER,
        TicketStatus.WAITING_FOR_APPROVAL,
        TicketStatus.CANCELLED
    },
    TicketStatus.ASSIGNED: {
        TicketStatus.IN_PROGRESS,
        TicketStatus.WAITING_FOR_USER,
        TicketStatus.WAITING_FOR_APPROVAL,
        TicketStatus.RESOLVED,
        TicketStatus.CANCELLED
    },
    TicketStatus.IN_PROGRESS: {
        TicketStatus.WAITING_FOR_USER,
        TicketStatus.WAITING_FOR_APPROVAL,
        TicketStatus.RESOLVED,
        TicketStatus.CANCELLED
    },
    TicketStatus.WAITING_FOR_USER: {
        TicketStatus.IN_PROGRESS,
        TicketStatus.RESOLVED,
        TicketStatus.CANCELLED
    },
    TicketStatus.WAITING_FOR_APPROVAL: {
        TicketStatus.IN_PROGRESS,
        TicketStatus.ASSIGNED,
        TicketStatus.RESOLVED,
        TicketStatus.CANCELLED
    },
    TicketStatus.RESOLVED: {
        TicketStatus.CLOSED,
        TicketStatus.REOPENED
    },
    TicketStatus.CLOSED: {
        TicketStatus.REOPENED
    },
    TicketStatus.REOPENED: {
        TicketStatus.IN_PROGRESS,
        TicketStatus.ASSIGNED,
        TicketStatus.RESOLVED,
        TicketStatus.CANCELLED
    },
    TicketStatus.CANCELLED: set()  # Terminal state
}


def validate_transition(current_status: str, new_status: str, user_role: str) -> None:
    try:
        curr_enum = TicketStatus(current_status)
        new_enum = TicketStatus(new_status)
    except ValueError:
        raise InvalidStateTransitionError(current_status, new_status)

    if curr_enum == new_enum:
        return

    allowed_targets = VALID_TRANSITIONS.get(curr_enum, set())
    if new_enum not in allowed_targets:
        # Admins can force transition if needed, otherwise block
        if user_role != "ADMIN":
            raise InvalidStateTransitionError(current_status, new_status)
