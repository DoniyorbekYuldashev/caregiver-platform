# Part 3: FastAPI application

from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal

from db import get_session
from models import User, Caregiver, Member, Job, Appointment
import crud

app = FastAPI(title="Caregiver Platform", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


# HOME & DASHBOARD

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    users_count = db.query(User).count()
    caregivers_count = db.query(Caregiver).count()
    members_count = db.query(Member).count()
    jobs_count = db.query(Job).count()
    appointments_count = db.query(Appointment).count()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "users_count": users_count,
        "caregivers_count": caregivers_count,
        "members_count": members_count,
        "jobs_count": jobs_count,
        "appointments_count": appointments_count
    })


# USER ROUTES

@app.get("/users", response_class=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.post("/users/create")
def create_user(
        email: str = Form(...),
        given_name: str = Form(...),
        surname: str = Form(...),
        city: str = Form(...),
        phone_number: str = Form(...),
        profile_description: str = Form(""),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    from schemas import UserCreate
    user = UserCreate(
        email=email,
        given_name=given_name,
        surname=surname,
        city=city,
        phone_number=phone_number,
        profile_description=profile_description,
        password=password
    )
    crud.create_user(db, user)
    return RedirectResponse("/users", status_code=303)


@app.post("/users/update/{user_id}")
def update_user(
        user_id: int,
        given_name: str = Form(...),
        surname: str = Form(...),
        city: str = Form(...),
        phone_number: str = Form(...),
        db: Session = Depends(get_db)
):
    from schemas import UserUpdate
    user = UserUpdate(given_name=given_name, surname=surname, city=city, phone_number=phone_number)
    crud.update_user(db, user_id, user)
    return RedirectResponse("/users", status_code=303)


@app.post("/users/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_user(db, user_id)
    except Exception as e:
        print(f"Error deleting user: {e}")
    return RedirectResponse("/users", status_code=303)


# CAREGIVER ROUTES

@app.get("/caregivers", response_class=HTMLResponse)
def list_caregivers(request: Request, db: Session = Depends(get_db)):
    caregivers = crud.get_caregivers(db)
    users = crud.get_users(db)
    return templates.TemplateResponse("caregivers.html", {
        "request": request,
        "caregivers": caregivers,
        "users": users
    })


@app.post("/caregivers/create")
def create_caregiver(
        caregiver_user_id: int = Form(...),
        gender: str = Form(...),
        caregiving_type: str = Form(...),
        hourly_rate: float = Form(...),
        photo: str = Form(""),
        db: Session = Depends(get_db)
):
    from schemas import CaregiverCreate
    caregiver = CaregiverCreate(
        caregiver_user_id=caregiver_user_id,
        gender=gender,
        caregiving_type=caregiving_type,
        hourly_rate=Decimal(str(hourly_rate)),
        photo=photo
    )
    crud.create_caregiver(db, caregiver)
    return RedirectResponse("/caregivers", status_code=303)


@app.post("/caregivers/update/{caregiver_id}")
def update_caregiver(
        caregiver_id: int,
        gender: str = Form(...),
        caregiving_type: str = Form(...),
        hourly_rate: float = Form(...),
        db: Session = Depends(get_db)
):
    from schemas import CaregiverUpdate
    caregiver = CaregiverUpdate(
        gender=gender,
        caregiving_type=caregiving_type,
        hourly_rate=Decimal(str(hourly_rate))
    )
    crud.update_caregiver(db, caregiver_id, caregiver)
    return RedirectResponse("/caregivers", status_code=303)


@app.post("/caregivers/delete/{caregiver_id}")
def delete_caregiver(caregiver_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_caregiver(db, caregiver_id)
    except Exception as e:
        print(f"Error deleting caregiver: {e}")
    return RedirectResponse("/caregivers", status_code=303)


# MEMBER ROUTES

@app.get("/members", response_class=HTMLResponse)
def list_members(request: Request, db: Session = Depends(get_db)):
    members = crud.get_members(db)
    users = crud.get_users(db)
    return templates.TemplateResponse("members.html", {
        "request": request,
        "members": members,
        "users": users
    })


@app.post("/members/create")
def create_member(
        member_user_id: int = Form(...),
        house_rules: str = Form(""),
        dependent_description: str = Form(""),
        db: Session = Depends(get_db)
):
    from schemas import MemberCreate
    member = MemberCreate(
        member_user_id=member_user_id,
        house_rules=house_rules,
        dependent_description=dependent_description
    )
    crud.create_member(db, member)
    return RedirectResponse("/members", status_code=303)


@app.post("/members/update/{member_id}")
def update_member(
        member_id: int,
        house_rules: str = Form(...),
        dependent_description: str = Form(...),
        db: Session = Depends(get_db)
):
    from schemas import MemberUpdate
    member = MemberUpdate(house_rules=house_rules, dependent_description=dependent_description)
    crud.update_member(db, member_id, member)
    return RedirectResponse("/members", status_code=303)


@app.post("/members/delete/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_member(db, member_id)
    except Exception as e:
        print(f"Error deleting member: {e}")
    return RedirectResponse("/members", status_code=303)


# JOB ROUTES

@app.get("/jobs", response_class=HTMLResponse)
def list_jobs(request: Request, db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db)
    members = crud.get_members(db)
    return templates.TemplateResponse("jobs.html", {
        "request": request,
        "jobs": jobs,
        "members": members
    })


@app.post("/jobs/create")
def create_job(
        member_user_id: int = Form(...),
        required_caregiving_type: str = Form(...),
        other_requirements: str = Form(""),
        db: Session = Depends(get_db)
):
    from schemas import JobCreate
    job = JobCreate(
        member_user_id=member_user_id,
        required_caregiving_type=required_caregiving_type,
        other_requirements=other_requirements
    )
    crud.create_job(db, job)
    return RedirectResponse("/jobs", status_code=303)


@app.post("/jobs/update/{job_id}")
def update_job(
        job_id: int,
        required_caregiving_type: str = Form(...),
        other_requirements: str = Form(...),
        db: Session = Depends(get_db)
):
    from schemas import JobUpdate
    job = JobUpdate(
        required_caregiving_type=required_caregiving_type,
        other_requirements=other_requirements
    )
    crud.update_job(db, job_id, job)
    return RedirectResponse("/jobs", status_code=303)


@app.post("/jobs/delete/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_job(db, job_id)
    except Exception as e:
        print(f"Error deleting job: {e}")
    return RedirectResponse("/jobs", status_code=303)


# APPOINTMENT ROUTES

@app.get("/appointments", response_class=HTMLResponse)
def list_appointments(request: Request, db: Session = Depends(get_db)):
    appointments = crud.get_appointments(db)
    caregivers = crud.get_caregivers(db)
    members = crud.get_members(db)
    return templates.TemplateResponse("appointments.html", {
        "request": request,
        "appointments": appointments,
        "caregivers": caregivers,
        "members": members
    })


@app.post("/appointments/create")
def create_appointment(
        caregiver_user_id: int = Form(...),
        member_user_id: int = Form(...),
        appointment_date: str = Form(...),
        appointment_time: str = Form(...),
        work_hours: float = Form(...),
        status: str = Form(...),
        db: Session = Depends(get_db)
):
    from schemas import AppointmentCreate
    appointment = AppointmentCreate(
        caregiver_user_id=caregiver_user_id,
        member_user_id=member_user_id,
        appointment_date=datetime.fromisoformat(appointment_date),
        appointment_time=appointment_time,
        work_hours=Decimal(str(work_hours)),
        status=status
    )
    crud.create_appointment(db, appointment)
    return RedirectResponse("/appointments", status_code=303)


@app.post("/appointments/update/{appointment_id}")
def update_appointment(
        appointment_id: int,
        appointment_date: str = Form(...),
        appointment_time: str = Form(...),
        work_hours: float = Form(...),
        status: str = Form(...),
        db: Session = Depends(get_db)
):
    from schemas import AppointmentUpdate
    appointment = AppointmentUpdate(
        appointment_date=datetime.fromisoformat(appointment_date),
        appointment_time=appointment_time,
        work_hours=Decimal(str(work_hours)),
        status=status
    )
    crud.update_appointment(db, appointment_id, appointment)
    return RedirectResponse("/appointments", status_code=303)


@app.post("/appointments/delete/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_appointment(db, appointment_id)
    except Exception as e:
        print(f"Error deleting appointment: {e}")
    return RedirectResponse("/appointments", status_code=303)


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)