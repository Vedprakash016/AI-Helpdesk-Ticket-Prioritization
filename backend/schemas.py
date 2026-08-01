from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10, max_length=5000)    

class TicketStatusUpdate(BaseModel):
    status: str    


class TicketAssign(BaseModel):
    agent_id: int    


class UserRoleUpdate(BaseModel):
    role: str    