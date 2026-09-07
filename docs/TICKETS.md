# Ticket Lifecycle & State Machine Specification

## Ticket States
- `NEW`: Newly created ticket pending initial routing.
- `OPEN`: Ticket routed to department queue.
- `ASSIGNED`: Agent claimed or assigned to ticket.
- `IN_PROGRESS`: Agent actively working on resolution.
- `WAITING_FOR_USER`: Waiting for employee response.
- `WAITING_FOR_APPROVAL`: Pending multi-step approval decision.
- `RESOLVED`: Resolution provided by agent.
- `CLOSED`: Employee or agent closed ticket.
- `REOPENED`: Employee reopened ticket due to recurring issue.
- `CANCELLED`: Ticket cancelled.
