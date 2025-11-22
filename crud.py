# Part 3: CRUD operations

from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import User, Caregiver, Member, Address, Job, JobApplication, Appointment
from schemas import *


# USER CRUD

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


# CAREGIVER CRUD

def create_caregiver(db: Session, caregiver: CaregiverCreate):
    db_caregiver = Caregiver(**caregiver.model_dump())
    db.add(db_caregiver)
    db.commit()
    db.refresh(db_caregiver)
    return db_caregiver


def get_caregivers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Caregiver).offset(skip).limit(limit).all()


def get_caregiver(db: Session, caregiver_id: int):
    return db.query(Caregiver).filter(Caregiver.caregiver_user_id == caregiver_id).first()


def update_caregiver(db: Session, caregiver_id: int, caregiver: CaregiverUpdate):
    db_caregiver = get_caregiver(db, caregiver_id)
    if db_caregiver:
        for key, value in caregiver.model_dump(exclude_unset=True).items():
            setattr(db_caregiver, key, value)
        db.commit()
        db.refresh(db_caregiver)
    return db_caregiver


def delete_caregiver(db: Session, caregiver_id: int):
    """Delete caregiver with all related records"""
    try:
        # Delete related job applications first
        db.query(JobApplication).filter(
            JobApplication.caregiver_user_id == caregiver_id
        ).delete(synchronize_session=False)

        # Delete related appointments
        db.query(Appointment).filter(
            Appointment.caregiver_user_id == caregiver_id
        ).delete(synchronize_session=False)

        # Now delete the caregiver
        db_caregiver = get_caregiver(db, caregiver_id)
        if db_caregiver:
            db.delete(db_caregiver)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise e


# MEMBER CRUD

def create_member(db: Session, member: MemberCreate):
    db_member = Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Member).offset(skip).limit(limit).all()


def get_member(db: Session, member_id: int):
    return db.query(Member).filter(Member.member_user_id == member_id).first()


def update_member(db: Session, member_id: int, member: MemberUpdate):
    db_member = get_member(db, member_id)
    if db_member:
        for key, value in member.model_dump(exclude_unset=True).items():
            setattr(db_member, key, value)
        db.commit()
        db.refresh(db_member)
    return db_member


def delete_member(db: Session, member_id: int):
    """Delete member with all related records"""
    try:
        # Delete related appointments
        db.query(Appointment).filter(
            Appointment.member_user_id == member_id
        ).delete(synchronize_session=False)

        # Delete related jobs (and their applications will cascade)
        db.query(Job).filter(
            Job.member_user_id == member_id
        ).delete(synchronize_session=False)

        # Delete address
        db.query(Address).filter(
            Address.member_user_id == member_id
        ).delete(synchronize_session=False)

        # Now delete the member
        db_member = get_member(db, member_id)
        if db_member:
            db.delete(db_member)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise e


# JOB CRUD

def create_job(db: Session, job: JobCreate):
    from datetime import datetime
    db_job = Job(**job.model_dump(), date_posted=datetime.now())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Job).offset(skip).limit(limit).all()


def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.job_id == job_id).first()


def update_job(db: Session, job_id: int, job: JobUpdate):
    db_job = get_job(db, job_id)
    if db_job:
        for key, value in job.model_dump(exclude_unset=True).items():
            setattr(db_job, key, value)
        db.commit()
        db.refresh(db_job)
    return db_job


def delete_job(db: Session, job_id: int):
    """Delete job with all related applications"""
    try:
        # Delete related job applications
        db.query(JobApplication).filter(
            JobApplication.job_id == job_id
        ).delete(synchronize_session=False)

        # Now delete the job
        db_job = get_job(db, job_id)
        if db_job:
            db.delete(db_job)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise e


# APPOINTMENT CRUD

def create_appointment(db: Session, appointment: AppointmentCreate):
    db_appointment = Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Appointment).offset(skip).limit(limit).all()


def get_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()


def update_appointment(db: Session, appointment_id: int, appointment: AppointmentUpdate):
    db_appointment = get_appointment(db, appointment_id)
    if db_appointment:
        for key, value in appointment.model_dump(exclude_unset=True).items():
            setattr(db_appointment, key, value)
        db.commit()
        db.refresh(db_appointment)
    return db_appointment


def delete_appointment(db: Session, appointment_id: int):
    db_appointment = get_appointment(db, appointment_id)
    if db_appointment:
        db.delete(db_appointment)
        db.commit()
        return True
    return False


# SEARCH & FILTER

def search_caregivers(db: Session, caregiving_type: str = None, city: str = None):
    query = db.query(Caregiver).join(User)
    if caregiving_type:
        query = query.filter(Caregiver.caregiving_type == caregiving_type)
    if city:
        query = query.filter(User.city == city)
    return query.all()


def get_accepted_appointments(db: Session):
    return db.query(Appointment).filter(
        or_(Appointment.status == 'confirmed', Appointment.status == 'completed')
    ).all()