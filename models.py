# Part 2

from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    given_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    profile_description = Column(Text)
    password = Column(String(255), nullable=False)
    caregiver = relationship("Caregiver", back_populates="user", uselist=False)
    member = relationship("Member", back_populates="user", uselist=False)

class Caregiver(Base):
    __tablename__ = "caregivers"
    caregiver_user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    photo = Column(String(500))
    gender = Column(String(20), nullable=False)
    caregiving_type = Column(String(50), nullable=False)
    hourly_rate = Column(DECIMAL(10, 2), nullable=False)
    user = relationship("User", back_populates="caregiver")
    job_applications = relationship("JobApplication", back_populates="caregiver")
    appointments = relationship("Appointment", back_populates="caregiver")

class Member(Base):
    __tablename__ = "members"
    member_user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    house_rules = Column(Text)
    dependent_description = Column(Text)
    user = relationship("User", back_populates="member")
    address = relationship("Address", back_populates="member", uselist=False)
    jobs = relationship("Job", back_populates="member")
    appointments = relationship("Appointment", back_populates="member")

class Address(Base):
    __tablename__ = "addresses"
    member_user_id = Column(Integer, ForeignKey("members.member_user_id", ondelete="CASCADE"), primary_key=True)
    house_number = Column(String(20), nullable=False)
    street = Column(String(200), nullable=False)
    town = Column(String(100), nullable=False)
    member = relationship("Member", back_populates="address")

class Job(Base):
    __tablename__ = "jobs"
    job_id = Column(Integer, primary_key=True)
    member_user_id = Column(Integer, ForeignKey("members.member_user_id", ondelete="CASCADE"), nullable=False)
    required_caregiving_type = Column(String(50), nullable=False)
    other_requirements = Column(Text)
    date_posted = Column(TIMESTAMP, nullable=False)
    member = relationship("Member", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job")

class JobApplication(Base):
    __tablename__ = "job_applications"
    caregiver_user_id = Column(Integer, ForeignKey("caregivers.caregiver_user_id", ondelete="CASCADE"), primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.job_id", ondelete="CASCADE"), primary_key=True)
    date_applied = Column(TIMESTAMP, nullable=False)
    caregiver = relationship("Caregiver", back_populates="job_applications")
    job = relationship("Job", back_populates="applications")

class Appointment(Base):
    __tablename__ = "appointments"
    appointment_id = Column(Integer, primary_key=True)
    caregiver_user_id = Column(Integer, ForeignKey("caregivers.caregiver_user_id", ondelete="CASCADE"), nullable=False)
    member_user_id = Column(Integer, ForeignKey("members.member_user_id", ondelete="CASCADE"), nullable=False)
    appointment_date = Column(TIMESTAMP, nullable=False)
    appointment_time = Column(String(10), nullable=False)
    work_hours = Column(DECIMAL(4, 2), nullable=False)
    status = Column(String(20), nullable=False)
    caregiver = relationship("Caregiver", back_populates="appointments")
    member = relationship("Member", back_populates="appointments")