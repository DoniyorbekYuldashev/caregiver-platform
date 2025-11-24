from sqlalchemy.orm import Session
from models import User, Caregiver, Member, Job, Appointment

# ============== USER CRUD ==============

def get_users(db: Session):
    return db.query(User).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def create_user(db: Session, email: str, given_name: str, surname: str, city: str, 
                phone_number: str, profile_description: str, password: str):
    user = User(
        email=email,
        given_name=given_name,
        surname=surname,
        city=city,
        phone_number=phone_number,
        profile_description=profile_description,
        password=password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_id: int, email: str, given_name: str, surname: str, 
                city: str, phone_number: str, profile_description: str, password: str):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.email = email
        user.given_name = given_name
        user.surname = surname
        user.city = city
        user.phone_number = phone_number
        user.profile_description = profile_description
        user.password = password
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

# ============== CAREGIVER CRUD ==============

def get_caregivers(db: Session):
    return db.query(Caregiver).all()

def get_caregiver(db: Session, caregiver_id: int):
    return db.query(Caregiver).filter(Caregiver.caregiver_id == caregiver_id).first()

def create_caregiver(db: Session, user_id: int, photo_url: str, gender: str, 
                     caregiving_type: str, hourly_rate: float):
    caregiver = Caregiver(
        user_id=user_id,
        photo_url=photo_url,
        gender=gender,
        caregiving_type=caregiving_type,
        hourly_rate=hourly_rate
    )
    db.add(caregiver)
    db.commit()
    db.refresh(caregiver)
    return caregiver

def update_caregiver(db: Session, caregiver_id: int, photo_url: str, gender: str, 
                     caregiving_type: str, hourly_rate: float):
    caregiver = db.query(Caregiver).filter(Caregiver.caregiver_id == caregiver_id).first()
    if caregiver:
        caregiver.photo_url = photo_url
        caregiver.gender = gender
        caregiver.caregiving_type = caregiving_type
        caregiver.hourly_rate = hourly_rate
        db.commit()
        db.refresh(caregiver)
    return caregiver

def delete_caregiver(db: Session, caregiver_id: int):
    caregiver = db.query(Caregiver).filter(Caregiver.caregiver_id == caregiver_id).first()
    if caregiver:
        db.delete(caregiver)
        db.commit()
    return caregiver

# ============== MEMBER CRUD ==============

def get_members(db: Session):
    return db.query(Member).all()

def get_member(db: Session, member_id: int):
    return db.query(Member).filter(Member.member_id == member_id).first()

def create_member(db: Session, user_id: int, house_rules: str):
    member = Member(
        user_id=user_id,
        house_rules=house_rules
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def update_member(db: Session, member_id: int, house_rules: str):
    member = db.query(Member).filter(Member.member_id == member_id).first()
    if member:
        member.house_rules = house_rules
        db.commit()
        db.refresh(member)
    return member

def delete_member(db: Session, member_id: int):
    member = db.query(Member).filter(Member.member_id == member_id).first()
    if member:
        db.delete(member)
        db.commit()
    return member

# ============== JOB CRUD ==============

def get_jobs(db: Session):
    return db.query(Job).all()

def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.job_id == job_id).first()

def create_job(db: Session, member_id: int, required_caregiving_type: str, other_requirements: str):
    job = Job(
        member_id=member_id,
        required_caregiving_type=required_caregiving_type,
        other_requirements=other_requirements
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def update_job(db: Session, job_id: int, required_caregiving_type: str, other_requirements: str):
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if job:
        job.required_caregiving_type = required_caregiving_type
        job.other_requirements = other_requirements
        db.commit()
        db.refresh(job)
    return job

def delete_job(db: Session, job_id: int):
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if job:
        db.delete(job)
        db.commit()
    return job

# ============== APPOINTMENT CRUD ==============

def get_appointments(db: Session):
    return db.query(Appointment).all()

def get_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()

def create_appointment(db: Session, caregiver_id: int, member_id: int, 
                       appointment_date: str, appointment_time: str, 
                       work_hours: float, status: str):
    from datetime import datetime
    appointment = Appointment(
        caregiver_id=caregiver_id,
        member_id=member_id,
        appointment_date=datetime.strptime(appointment_date, '%Y-%m-%d').date(),
        appointment_time=appointment_time,
        work_hours=work_hours,
        status=status
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

def update_appointment(db: Session, appointment_id: int, appointment_date: str, 
                       appointment_time: str, work_hours: float, status: str):
    from datetime import datetime
    appointment = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if appointment:
        appointment.appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        appointment.appointment_time = appointment_time
        appointment.work_hours = work_hours
        appointment.status = status
        db.commit()
        db.refresh(appointment)
    return appointment

def delete_appointment(db: Session, appointment_id: int):
    appointment = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if appointment:
        db.delete(appointment)
        db.commit()
    return appointment