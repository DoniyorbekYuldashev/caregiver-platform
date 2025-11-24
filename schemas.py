# Part 3: Pydantic schemas

"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from decimal import Decimal

class UserBase(BaseModel):
    email: EmailStr
    given_name: str
    surname: str
    city: str
    phone_number: str
    profile_description: Optional[str] = None
    password: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    given_name: Optional[str] = None
    surname: Optional[str] = None
    city: Optional[str] = None
    phone_number: Optional[str] = None
    profile_description: Optional[str] = None

class UserResponse(UserBase):
    user_id: int
    class Config:
        from_attributes = True

class CaregiverBase(BaseModel):
    photo: Optional[str] = None
    gender: str
    caregiving_type: str
    hourly_rate: Decimal

class CaregiverCreate(CaregiverBase):
    caregiver_user_id: int

class CaregiverUpdate(BaseModel):
    photo: Optional[str] = None
    gender: Optional[str] = None
    caregiving_type: Optional[str] = None
    hourly_rate: Optional[Decimal] = None

class CaregiverResponse(CaregiverBase):
    caregiver_user_id: int
    class Config:
        from_attributes = True

class MemberBase(BaseModel):
    house_rules: Optional[str] = None
    dependent_description: Optional[str] = None

class MemberCreate(MemberBase):
    member_user_id: int

class MemberUpdate(MemberBase):
    pass

class MemberResponse(MemberBase):
    member_user_id: int
    class Config:
        from_attributes = True

class JobBase(BaseModel):
    required_caregiving_type: str
    other_requirements: Optional[str] = None

class JobCreate(JobBase):
    member_user_id: int

class JobUpdate(BaseModel):
    required_caregiving_type: Optional[str] = None
    other_requirements: Optional[str] = None

class JobResponse(JobBase):
    job_id: int
    member_user_id: int
    date_posted: datetime
    class Config:
        from_attributes = True

class AppointmentBase(BaseModel):
    appointment_date: datetime
    appointment_time: str
    work_hours: Decimal
    status: str

class AppointmentCreate(AppointmentBase):
    caregiver_user_id: int
    member_user_id: int

class AppointmentUpdate(BaseModel):
    appointment_date: Optional[datetime] = None
    appointment_time: Optional[str] = None
    work_hours: Optional[Decimal] = None
    status: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    appointment_id: int
    caregiver_user_id: int
    member_user_id: int
    class Config:
        from_attributes = True