from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class VisitorBase(BaseModel):
    visitorName: str = Field(..., min_length=1)
    visitorPhoneNumber: str = Field(..., pattern="^[0-9]{10}$")
    visitorDriverLicenseNumber: Optional[str] = None
    visitorCompanyName: Optional[str] = None
    comingFrom: Optional[str] = None

class EmployeeBase(BaseModel):
    employeeName: str = Field(..., min_length=1)
    department: Optional[str] = None
    phoneNumber: str = Field(..., pattern="^[0-9]{10}$")
    designation: Optional[str] = None

class VisitBase(BaseModel):
    visitDate: str
    visitorPhoneNumber: str = Field(..., pattern="^[0-9]{10}$")
    employeePhoneNumber: str = Field(..., pattern="^[0-9]{10}$")
    purposeOfVisit: str
    visitDuration: int = Field(..., ge=1, le=480)
    comments: Optional[str] = None

class EmployeeDB(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    department: Optional[str] = Field(None, max_length=50)
    role: Optional[str] = Field(None, max_length=50)

class VisitorDB(BaseModel):
    id: Optional[int] = None
    visitorName: str = Field(..., min_length=1, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    purpose: Optional[str] = Field(None, max_length=200)
    checkInTime: Optional[str] = None
    checkOutTime: Optional[str] = None
    hostEmployeeId: Optional[int] = None

class VisitDB(BaseModel):
    id: Optional[int] = None
    visitor_id: int
    employee_id: int
    check_in_time: str
    check_out_time: Optional[str] = None
    purpose: Optional[str] = Field(None, max_length=200)

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
