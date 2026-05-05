from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Employee(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    department: Optional[str] = Field(None, max_length=50)
    role: Optional[str] = Field(None, max_length=50)

class Visitor(BaseModel):
    id: Optional[int] = None
    visitorName: str = Field(..., min_length=1, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    purpose: Optional[str] = Field(None, max_length=200)
    checkInTime: Optional[str] = None
    checkOutTime: Optional[str] = None
    hostEmployeeId: Optional[int] = None

class Visit(BaseModel):
    id: Optional[int] = None
    visitor_id: int
    employee_id: int
    check_in_time: str
    check_out_time: Optional[str] = None
    purpose: Optional[str] = Field(None, max_length=200)

# Request models
class CreateEmployeeRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    department: Optional[str] = Field(None, max_length=50)
    role: Optional[str] = Field(None, max_length=50)

class CreateVisitorRequest(BaseModel):
    visitorName: str = Field(..., min_length=1, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    purpose: Optional[str] = Field(None, max_length=200)
    checkInTime: Optional[str] = None
    checkOutTime: Optional[str] = None
    hostEmployeeId: Optional[int] = None

class CreateVisitRequest(BaseModel):
    visitor_id: int
    employee_id: int
    check_in_time: str
    check_out_time: Optional[str] = None
    purpose: Optional[str] = Field(None, max_length=200)

class UpdateEmployeeRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    department: Optional[str] = Field(None, max_length=50)
    role: Optional[str] = Field(None, max_length=50)

class UpdateVisitorRequest(BaseModel):
    visitorName: Optional[str] = Field(None, min_length=1, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    purpose: Optional[str] = Field(None, max_length=200)
    checkInTime: Optional[str] = None
    checkOutTime: Optional[str] = None
    hostEmployeeId: Optional[int] = None

class UpdateVisitRequest(BaseModel):
    check_out_time: Optional[str] = None
    purpose: Optional[str] = Field(None, max_length=200)

# Response models
class StandardResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str