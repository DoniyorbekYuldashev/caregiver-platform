from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    given_name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=False)
    profile_description = Column(Text)
    password = Column(String(100), nullable=False)

    # Relationships
    caregiver = relationship("Caregiver", back_populates="user", uselist=False, cascade="all, delete-orphan")
    member = relationship("Member", back_populates="user", uselist=False, cascade="all, delete-orphan")
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")

class Caregiver(Base):
    __tablename__ = 'caregivers'

    caregiver_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, unique=True)
    photo_url = Column(String(255))
    gender = Column(String(20))
    caregiving_type = Column(String(50), nullable=False)
    hourly_rate = Column(Float, nullable=False)

    # Relationships
    user = relationship("User", back_populates="caregiver")
    appointments = relationship("Appointment", back_populates="caregiver", cascade="all, delete-orphan")
    job_applications = relationship("JobApplication", back_populates="caregiver", cascade="all, delete-orphan")


class Member(Base):
    __tablename__ = 'members'

    member_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, unique=True)
    house_rules = Column(Text)

    # Relationships
    user = relationship("User", back_populates="member")
    jobs = relationship("Job", back_populates="member", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="member", cascade="all, delete-orphan")


class Job(Base):
    __tablename__ = 'jobs'

    job_id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('members.member_id', ondelete='CASCADE'), nullable=False)
    required_caregiving_type = Column(String(50), nullable=False)
    other_requirements = Column(Text)
    date_posted = Column(DateTime, default=datetime.utcnow)

    # Relationships
    member = relationship("Member", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")


class Appointment(Base):
    __tablename__ = 'appointments'

    appointment_id = Column(Integer, primary_key=True, autoincrement=True)
    caregiver_id = Column(Integer, ForeignKey('caregivers.caregiver_id', ondelete='CASCADE'), nullable=False)
    member_id = Column(Integer, ForeignKey('members.member_id', ondelete='CASCADE'), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(String(10), nullable=False)
    work_hours = Column(Float, nullable=False)
    status = Column(String(20), nullable=False)

    # Relationships
    caregiver = relationship("Caregiver", back_populates="appointments")
    member = relationship("Member", back_populates="appointments")


class Address(Base):
    __tablename__ = 'addresses'

    address_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    street_address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state_province = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100), nullable=False)

    # Relationship
    user = relationship("User", back_populates="addresses")


class JobApplication(Base):
    __tablename__ = 'job_applications'

    application_id = Column(Integer, primary_key=True, autoincrement=True)
    caregiver_id = Column(Integer, ForeignKey('caregivers.caregiver_id', ondelete='CASCADE'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.job_id', ondelete='CASCADE'), nullable=False)
    date_applied = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(50), default='pending', nullable=False)  # pending, accepted, rejected
    cover_letter = Column(Text)

    # Relationships
    caregiver = relationship("Caregiver", back_populates="job_applications")
    job = relationship("Job", back_populates="applications")