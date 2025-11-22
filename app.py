from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from models import Base, User, Caregiver, Member, Job, Appointment
import crud

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")

# Create engine
engine = create_engine(DATABASE_URL)

print("Dropping existing tables...")
Base.metadata.drop_all(bind=engine)
print("Creating fresh tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI app
app = FastAPI(title="Caregiver Platform - CSCI 341")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    db = SessionLocal()
    try:
        users_count = db.query(User).count()
        caregivers_count = db.query(Caregiver).count()
        members_count = db.query(Member).count()
        jobs_count = db.query(Job).count()
        appointments_count = db.query(Appointment).count()
    except Exception as e:
        print(f"Error counting: {e}")
        users_count = caregivers_count = members_count = jobs_count = appointments_count = 0
    finally:
        db.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "users_count": users_count,
        "caregivers_count": caregivers_count,
        "members_count": members_count,
        "jobs_count": jobs_count,
        "appointments_count": appointments_count
    })


@app.get("/users", response_class=HTMLResponse)
async def list_users(request: Request):
    db = SessionLocal()
    users = crud.get_users(db)
    db.close()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/users/create", response_class=HTMLResponse)
async def create_user_form(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": [], "show_form": True})


@app.post("/users/create")
async def create_user(
        email: str = Form(...),
        given_name: str = Form(...),
        surname: str = Form(...),
        city: str = Form(...),
        phone_number: str = Form(...),
        profile_description: str = Form(...),
        password: str = Form(...)
):
    db = SessionLocal()
    crud.create_user(db, email, given_name, surname, city, phone_number, profile_description, password)
    db.close()
    return RedirectResponse(url="/users", status_code=303)


@app.get("/users/edit/{user_id}", response_class=HTMLResponse)
async def edit_user_form(request: Request, user_id: int):
    db = SessionLocal()
    user = crud.get_user(db, user_id)
    users = crud.get_users(db)
    db.close()
    return templates.TemplateResponse("users.html", {
        "request": request,
        "users": users,
        "edit_user": user
    })


@app.post("/users/edit/{user_id}")
async def edit_user(
        user_id: int,
        email: str = Form(...),
        given_name: str = Form(...),
        surname: str = Form(...),
        city: str = Form(...),
        phone_number: str = Form(...),
        profile_description: str = Form(...),
        password: str = Form(...)
):
    db = SessionLocal()
    crud.update_user(db, user_id, email, given_name, surname, city, phone_number, profile_description, password)
    db.close()
    return RedirectResponse(url="/users", status_code=303)


@app.api_route("/users/delete/{user_id}", methods=["GET", "POST"])
async def delete_user(user_id: int):
    db = SessionLocal()
    crud.delete_user(db, user_id)
    db.close()
    return RedirectResponse(url="/users", status_code=303)


@app.get("/caregivers", response_class=HTMLResponse)
async def list_caregivers(request: Request):
    db = SessionLocal()
    caregivers = crud.get_caregivers(db)
    users = crud.get_users(db)
    db.close()
    return templates.TemplateResponse("caregivers.html", {
        "request": request,
        "caregivers": caregivers,
        "users": users
    })


@app.post("/caregivers/create")
async def create_caregiver(
        user_id: int = Form(...),
        photo_url: str = Form(...),
        gender: str = Form(...),
        caregiving_type: str = Form(...),
        hourly_rate: float = Form(...)
):
    db = SessionLocal()
    crud.create_caregiver(db, user_id, photo_url, gender, caregiving_type, hourly_rate)
    db.close()
    return RedirectResponse(url="/caregivers", status_code=303)


@app.post("/caregivers/edit/{caregiver_id}")
async def edit_caregiver(
        caregiver_id: int,
        photo_url: str = Form(...),
        gender: str = Form(...),
        caregiving_type: str = Form(...),
        hourly_rate: float = Form(...)
):
    db = SessionLocal()
    crud.update_caregiver(db, caregiver_id, photo_url, gender, caregiving_type, hourly_rate)
    db.close()
    return RedirectResponse(url="/caregivers", status_code=303)


@app.api_route("/caregivers/delete/{caregiver_id}", methods=["GET", "POST"])
async def delete_caregiver(caregiver_id: int):
    db = SessionLocal()
    crud.delete_caregiver(db, caregiver_id)
    db.close()
    return RedirectResponse(url="/caregivers", status_code=303)


@app.get("/members", response_class=HTMLResponse)
async def list_members(request: Request):
    db = SessionLocal()
    members = crud.get_members(db)
    users = crud.get_users(db)
    db.close()
    return templates.TemplateResponse("members.html", {
        "request": request,
        "members": members,
        "users": users
    })


@app.post("/members/create")
async def create_member(
        user_id: int = Form(...),
        house_rules: str = Form(...)
):
    db = SessionLocal()
    crud.create_member(db, user_id, house_rules)
    db.close()
    return RedirectResponse(url="/members", status_code=303)


@app.post("/members/edit/{member_id}")
async def edit_member(
        member_id: int,
        house_rules: str = Form(...)
):
    db = SessionLocal()
    crud.update_member(db, member_id, house_rules)
    db.close()
    return RedirectResponse(url="/members", status_code=303)


@app.api_route("/members/delete/{member_id}", methods=["GET", "POST"])
async def delete_member(member_id: int):
    db = SessionLocal()
    crud.delete_member(db, member_id)
    db.close()
    return RedirectResponse(url="/members", status_code=303)


@app.get("/jobs", response_class=HTMLResponse)
async def list_jobs(request: Request):
    db = SessionLocal()
    jobs = crud.get_jobs(db)
    members = crud.get_members(db)
    db.close()
    return templates.TemplateResponse("jobs.html", {
        "request": request,
        "jobs": jobs,
        "members": members
    })


@app.post("/jobs/create")
async def create_job(
        member_id: int = Form(...),
        required_caregiving_type: str = Form(...),
        other_requirements: str = Form(...)
):
    db = SessionLocal()
    crud.create_job(db, member_id, required_caregiving_type, other_requirements)
    db.close()
    return RedirectResponse(url="/jobs", status_code=303)


@app.post("/jobs/edit/{job_id}")
async def edit_job(
        job_id: int,
        required_caregiving_type: str = Form(...),
        other_requirements: str = Form(...)
):
    db = SessionLocal()
    crud.update_job(db, job_id, required_caregiving_type, other_requirements)
    db.close()
    return RedirectResponse(url="/jobs", status_code=303)


@app.api_route("/jobs/delete/{job_id}", methods=["GET", "POST"])
async def delete_job(job_id: int):
    db = SessionLocal()
    crud.delete_job(db, job_id)
    db.close()
    return RedirectResponse(url="/jobs", status_code=303)


@app.get("/appointments", response_class=HTMLResponse)
async def list_appointments(request: Request):
    db = SessionLocal()
    appointments = crud.get_appointments(db)
    caregivers = crud.get_caregivers(db)
    members = crud.get_members(db)
    db.close()
    return templates.TemplateResponse("appointments.html", {
        "request": request,
        "appointments": appointments,
        "caregivers": caregivers,
        "members": members
    })


@app.post("/appointments/create")
async def create_appointment(
        caregiver_id: int = Form(...),
        member_id: int = Form(...),
        appointment_date: str = Form(...),
        appointment_time: str = Form(...),
        work_hours: float = Form(...),
        status: str = Form(...)
):
    db = SessionLocal()
    crud.create_appointment(db, caregiver_id, member_id, appointment_date, appointment_time, work_hours, status)
    db.close()
    return RedirectResponse(url="/appointments", status_code=303)


@app.post("/appointments/edit/{appointment_id}")
async def edit_appointment(
        appointment_id: int,
        appointment_date: str = Form(...),
        appointment_time: str = Form(...),
        work_hours: float = Form(...),
        status: str = Form(...)
):
    db = SessionLocal()
    crud.update_appointment(db, appointment_id, appointment_date, appointment_time, work_hours, status)
    db.close()
    return RedirectResponse(url="/appointments", status_code=303)


@app.api_route("/appointments/delete/{appointment_id}", methods=["GET", "POST"])
async def delete_appointment(appointment_id: int):
    db = SessionLocal()
    crud.delete_appointment(db, appointment_id)
    db.close()
    return RedirectResponse(url="/appointments", status_code=303)