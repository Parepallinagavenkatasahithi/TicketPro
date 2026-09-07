from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.models.ticket import Ticket, TicketCategory, TicketStatus, TicketAssignment
from app.models.department import Department


class TicketRoutingService:
    def __init__(self, db: Session):
        self.db = db

    def route_and_assign_ticket(self, ticket: Ticket) -> Optional[User]:
        # 1. Determine Department if missing
        if not ticket.department_id:
            category = self.db.query(TicketCategory).filter(TicketCategory.id == ticket.category_id).first()
            if category and category.default_department_id:
                ticket.department_id = category.default_department_id
            else:
                # Default to IT Department
                it_dept = self.db.query(Department).filter(Department.code == "IT").first()
                if it_dept:
                    ticket.department_id = it_dept.id

        # 2. Find eligible active agents in the target department
        eligible_agents = self.db.query(User).filter(
            User.is_active == True,
            User.role_name.in_(["AGENT", "MANAGER", "ADMIN"])
        )
        if ticket.department_id:
            dept_agents = eligible_agents.filter(User.department_id == ticket.department_id).all()
            if dept_agents:
                eligible_agents = dept_agents
            else:
                eligible_agents = eligible_agents.all()
        else:
            eligible_agents = eligible_agents.all()

        if not eligible_agents:
            return None

        # 3. Workload Balancing Selection: Pick agent with fewest active/in-progress tickets
        agent_workloads = []
        for agent in eligible_agents:
            active_count = self.db.query(func.count(Ticket.id)).filter(
                Ticket.assigned_agent_id == agent.id,
                Ticket.status.in_([TicketStatus.ASSIGNED.value, TicketStatus.IN_PROGRESS.value])
            ).scalar() or 0
            agent_workloads.append((active_count, agent))

        agent_workloads.sort(key=lambda x: x[0])
        selected_agent = agent_workloads[0][1]

        # Assign ticket
        ticket.assigned_agent_id = selected_agent.id
        ticket.status = TicketStatus.ASSIGNED.value

        # Record assignment log
        assignment = TicketAssignment(
            ticket_id=ticket.id,
            agent_id=selected_agent.id,
            assigned_by_id=ticket.requester_id,
            reason="Automated Intelligent Routing & Workload Balancing"
        )
        self.db.add(assignment)
        self.db.commit()

        return selected_agent
