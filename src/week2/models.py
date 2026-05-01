from pydantic import BaseModel, Field
from typing import Optional

class Visitor(BaseModel):
    visitorName: str = Field(..., min_length=1)
    visitorPhoneNumber: str = Field(..., pattern="^[0-9]{10}$")
    visitorDriverLicenseNumber: Optional[str] = None
    visitorCompanyName: Optional[str] = None
    comingFrom: Optional[str] = None

class Employee(BaseModel):
    employeeName: str = Field(..., min_length=1)
    department: Optional[str] = None
    phoneNumber: str = Field(..., pattern="^[0-9]{10}$")
    designation: Optional[str] = None

class Visit(BaseModel):
    visitDate: str
    visitorPhoneNumber: str = Field(..., pattern="^[0-9]{10}$")
    employeePhoneNumber: str = Field(..., pattern="^[0-9]{10}$")
    purposeOfVisit: str
    visitDuration: int = Field(..., ge=1, le=480)
    comments: Optional[str] = None
