import pytest
from app.domain.state_machine import validate_transition
from app.core.exceptions import InvalidStateTransitionError

def test_valid_transitions():
    validate_transition("NEW", "OPEN", "AGENT")
    validate_transition("OPEN", "ASSIGNED", "AGENT")
    validate_transition("ASSIGNED", "IN_PROGRESS", "AGENT")
    validate_transition("IN_PROGRESS", "RESOLVED", "AGENT")
    validate_transition("RESOLVED", "CLOSED", "AGENT")
    validate_transition("CLOSED", "REOPENED", "EMPLOYEE")

def test_invalid_transition_blocked():
    with pytest.raises(InvalidStateTransitionError):
        validate_transition("NEW", "CLOSED", "EMPLOYEE")
