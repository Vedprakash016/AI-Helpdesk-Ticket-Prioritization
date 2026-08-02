from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from ai_service import predict_ticket
from fastapi.middleware.cors import CORSMiddleware

import models
import schemas
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    check_role
)
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
security = HTTPBearer()

app = FastAPI(
    title="AI Helpdesk Ticket Prioritization System",
    description="Backend API for the AI-based Helpdesk Ticket Prioritization System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
   allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "https://ai-helpdesk-ticket-prioritization-qdqe7m1bj-voyager-x1.vercel.app",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AI Helpdesk Backend is running successfully!"
    }


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role
        }
    }

@app.post("/login")
def login_user(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    db_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": str(db_user.id),
            "role": db_user.role
        }
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email,
            "role": db_user.role
        }
    }

@app.get("/users/me")
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = (
        db.query(models.User)
        .filter(models.User.id == int(user_id))
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }


@app.post("/tickets", status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket: schemas.TicketCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = (
        db.query(models.User)
        .filter(models.User.id == int(user_id))
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    ai_result = predict_ticket(
        ticket.title,
        ticket.description
    )

    new_ticket = models.Ticket(
        title=ticket.title,
        description=ticket.description,
        category=ai_result["category"],
        priority=ai_result["priority"],
        priority_score=ai_result["priority_score"],
        status="Open",
        created_by=user.id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {
        "message": "Ticket created successfully",
        "ticket": {
            "id": new_ticket.id,
            "title": new_ticket.title,
            "description": new_ticket.description,
            "category": new_ticket.category,
            "priority": new_ticket.priority,
            "priority_score": new_ticket.priority_score,
            "status": new_ticket.status,
            "created_by": new_ticket.created_by
        }
    }


@app.get("/tickets/my")
def get_my_tickets(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    tickets = (
        db.query(models.Ticket)
        .filter(models.Ticket.created_by == int(user_id))
        .order_by(models.Ticket.created_at.desc())
        .all()
    )

    return {
        "total": len(tickets),
        "tickets": [
            {
                "id": ticket.id,
                "title": ticket.title,
                "description": ticket.description,
                "category": ticket.category,
                "priority": ticket.priority,
                "priority_score": ticket.priority_score,
                "status": ticket.status,
                "created_at": ticket.created_at
            }
            for ticket in tickets
        ]
    }


@app.get("/tickets/{ticket_id}")
def get_ticket(
    ticket_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(credentials.credentials)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    ticket = (
        db.query(models.Ticket)
        .filter(
            models.Ticket.id == ticket_id,
            models.Ticket.created_by == int(user_id)
        )
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    return {
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "category": ticket.category,
        "priority": ticket.priority,
        "priority_score": ticket.priority_score,
        "status": ticket.status,
        "created_by": ticket.created_by,
        "assigned_agent": ticket.assigned_agent,
        "created_at": ticket.created_at
    }


@app.patch("/tickets/{ticket_id}/status")
def update_ticket_status(
    ticket_id: int,
    status_update: schemas.TicketStatusUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(credentials.credentials)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    if not check_role(payload, ["agent", "admin"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only agents or admins can update ticket status"
        )

    allowed_statuses = [
        "Open",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    if status_update.status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket status"
        )

    ticket = (
        db.query(models.Ticket)
        .filter(models.Ticket.id == ticket_id)
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    ticket.status = status_update.status

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket status updated successfully",
        "ticket": {
            "id": ticket.id,
            "title": ticket.title,
            "status": ticket.status,
            "priority": ticket.priority
        }
    }


@app.get("/agent/tickets")
def get_all_tickets(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(credentials.credentials)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    if not check_role(payload, ["agent", "admin"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only agents or admins can view all tickets"
        )

    tickets = (
        db.query(models.Ticket)
        .order_by(models.Ticket.created_at.desc())
        .all()
    )

    return {
        "total": len(tickets),
        "tickets": [
            {
                "id": ticket.id,
                "title": ticket.title,
                "description": ticket.description,
                "category": ticket.category,
                "priority": ticket.priority,
                "priority_score": ticket.priority_score,
                "status": ticket.status,
                "created_by": ticket.created_by,
                "assigned_agent": ticket.assigned_agent,
                "created_at": ticket.created_at
            }
            for ticket in tickets
        ]
    }


@app.patch("/tickets/{ticket_id}/assign")
def assign_ticket(
    ticket_id: int,
    assignment: schemas.TicketAssign,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(credentials.credentials)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    if not check_role(payload, ["agent", "admin"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only agents or admins can assign tickets"
        )

    ticket = (
        db.query(models.Ticket)
        .filter(models.Ticket.id == ticket_id)
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    agent = (
        db.query(models.User)
        .filter(
            models.User.id == assignment.agent_id,
            models.User.role == "agent"
        )
        .first()
    )

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )

    ticket.assigned_agent = agent.id

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket assigned successfully",
        "ticket": {
            "id": ticket.id,
            "title": ticket.title,
            "status": ticket.status,
            "assigned_agent": ticket.assigned_agent
        },
        "agent": {
            "id": agent.id,
            "name": agent.name,
            "email": agent.email
        }
    }


@app.get("/agent/tickets/assigned")
def get_assigned_tickets(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(credentials.credentials)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    if not check_role(payload, ["agent", "admin"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only agents or admins can access assigned tickets"
        )

    user_id = int(payload.get("sub"))

    tickets = (
        db.query(models.Ticket)
        .filter(models.Ticket.assigned_agent == user_id)
        .order_by(models.Ticket.created_at.desc())
        .all()
    )

    return {
        "total": len(tickets),
        "tickets": [
            {
                "id": ticket.id,
                "title": ticket.title,
                "category": ticket.category,
                "priority": ticket.priority,
                "priority_score": ticket.priority_score,
                "status": ticket.status,
                "created_by": ticket.created_by,
                "created_at": ticket.created_at
            }
            for ticket in tickets
        ]
    }


@app.get("/admin/stats")
def admin_stats(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(credentials.credentials)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    if not check_role(payload, ["admin"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    total_users = db.query(models.User).count()

    total_agents = (
        db.query(models.User)
        .filter(models.User.role == "agent")
        .count()
    )

    total_tickets = db.query(models.Ticket).count()

    open_tickets = (
        db.query(models.Ticket)
        .filter(models.Ticket.status == "Open")
        .count()
    )

    in_progress = (
        db.query(models.Ticket)
        .filter(models.Ticket.status == "In Progress")
        .count()
    )

    resolved = (
        db.query(models.Ticket)
        .filter(models.Ticket.status == "Resolved")
        .count()
    )

    closed = (
        db.query(models.Ticket)
        .filter(models.Ticket.status == "Closed")
        .count()
    )

    critical = (
        db.query(models.Ticket)
        .filter(models.Ticket.priority == "Critical")
        .count()
    )

    return {
        "total_users": total_users,
        "total_agents": total_agents,
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress,
        "resolved_tickets": resolved,
        "closed_tickets": closed,
        "critical_tickets": critical
    }


@app.get("/admin/users")
def get_all_users(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(credentials.credentials)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    if not check_role(payload, ["admin"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    users = (
        db.query(models.User)
        .order_by(models.User.id.asc())
        .all()
    )

    return {
        "total": len(users),
        "users": [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
            for user in users
        ]
    }


@app.patch("/admin/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role_update: schemas.UserRoleUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(credentials.credentials)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    if not check_role(payload, ["admin"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    allowed_roles = ["user", "agent", "admin"]

    if role_update.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )

    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.role = role_update.role

    db.commit()
    db.refresh(user)

    return {
        "message": "User role updated successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }


@app.get("/admin/agents")
def get_all_agents(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(credentials.credentials)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    if not check_role(payload, ["admin"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    agents = (
        db.query(models.User)
        .filter(models.User.role == "agent")
        .order_by(models.User.name.asc())
        .all()
    )

    return {
        "total": len(agents),
        "agents": [
            {
                "id": agent.id,
                "name": agent.name,
                "email": agent.email
            }
            for agent in agents
        ]
    }