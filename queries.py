# Part 2

from sqlalchemy import func, and_, or_, text
from tabulate import tabulate
from models import User, Caregiver, Member, Address, Job, JobApplication, Appointment
from decimal import Decimal


def print_results(headers, rows, message=""):
    if message:
        print(f"\n{message}")
    if rows:
        print(f"\nFound {len(rows)} result(s):\n")
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("(No results)")


# 3. UPDATE QUERIES
def update_3_1_phone_number(session):
    print(f"3.1 UPDATE: Arman Armanov's phone number")

    user = session.query(User).filter(User.given_name == 'Arman', User.surname == 'Armanov').first()
    if user:
        old_phone = user.phone_number
        user.phone_number = '+77773414141'
        session.commit()
        print(f"\n✓ Updated: {old_phone} → {user.phone_number}")

        result = session.query(User.user_id, User.given_name, User.surname, User.phone_number) \
            .filter(User.user_id == user.user_id).first()
        print_results(['User ID', 'First Name', 'Last Name', 'Phone'], [result])


def update_3_2_commission_fee(session):
    print(f"3.2 UPDATE: Add commission to hourly rates")

    before = session.query(Caregiver.caregiver_user_id, User.given_name, User.surname, Caregiver.hourly_rate) \
        .join(User).all()
    print("\nBefore:")
    print_results(['ID', 'Name', 'Old Rate'],
                  [[r[0], f"{r[1]} {r[2]}", f"${r[3]:.2f}"] for r in before])

    caregivers = session.query(Caregiver).all()
    for c in caregivers:
        c.hourly_rate = c.hourly_rate + Decimal('0.30') if c.hourly_rate < 10 else c.hourly_rate * Decimal('1.10')
    session.commit()

    after = session.query(Caregiver.caregiver_user_id, User.given_name, User.surname, Caregiver.hourly_rate) \
        .join(User).all()
    print(f"\n✓ Updated {len(caregivers)} caregiver(s)\n\nAfter:")
    print_results(['ID', 'Name', 'New Rate'],
                  [[r[0], f"{r[1]} {r[2]}", f"${r[3]:.2f}"] for r in after])



# 4. DELETE QUERIES
def delete_4_1_jobs_by_amina(session):
    print(f"4.1 DELETE: Jobs by Amina Aminova")

    amina = session.query(User).filter(User.given_name == 'Amina', User.surname == 'Aminova').first()
    if amina:
        jobs = session.query(Job.job_id, Job.required_caregiving_type, Job.other_requirements) \
            .filter(Job.member_user_id == amina.user_id).all()
        print(f"\nJobs before deletion:")
        print_results(['Job ID', 'Type', 'Requirements'],
                      [[j[0], j[1], j[2][:50] + '...'] for j in jobs])

        deleted = session.query(Job).filter(Job.member_user_id == amina.user_id).delete()
        session.commit()
        print(f"\nDeleted {deleted} job(s)")


def delete_4_2_members_on_kabanbay_batyr(session):
    print(f"4.2 DELETE: Members on Kabanbay Batyr street")

    members = session.query(User.user_id, User.given_name, User.surname, Address.street, Address.town) \
        .join(Member, User.user_id == Member.member_user_id) \
        .join(Address, Member.member_user_id == Address.member_user_id) \
        .filter(Address.street == 'Kabanbay Batyr').all()

    print("\nMembers before deletion:")
    print_results(['ID', 'Name', 'Street', 'Town'],
                  [[m[0], f"{m[1]} {m[2]}", m[3], m[4]] for m in members])

    if members:
        member_ids = [m[0] for m in members]
        deleted = session.query(Member).filter(Member.member_user_id.in_(member_ids)).delete(synchronize_session=False)
        session.commit()
        print(f"\nDeleted {deleted} member(s)")


# 5. SIMPLE QUERIES
def query_5_1_accepted_appointments(session):
    print(f"5.1 SELECT: Accepted appointments")

    results = session.execute(text("""
        SELECT a.appointment_id, 
               uc.given_name || ' ' || uc.surname AS caregiver_name,
               um.given_name || ' ' || um.surname AS member_name,
               a.status, a.appointment_date
        FROM appointments a
        JOIN caregivers c ON a.caregiver_user_id = c.caregiver_user_id
        JOIN users uc ON c.caregiver_user_id = uc.user_id
        JOIN members m ON a.member_user_id = m.member_user_id
        JOIN users um ON m.member_user_id = um.user_id
        WHERE a.status IN ('confirmed', 'completed')
        ORDER BY a.appointment_id
    """)).fetchall()

    print_results(['ID', 'Caregiver', 'Member', 'Status', 'Date'], results)


def query_5_2_jobs_with_soft_spoken(session):
    print(f"5.2 SELECT: Jobs with 'soft-spoken'")

    results = session.query(Job.job_id, Job.required_caregiving_type, Job.other_requirements) \
        .filter(Job.other_requirements.like('%soft-spoken%')).all()

    print_results(['Job ID', 'Type', 'Requirements'],
                  [[r[0], r[1], r[2][:60] + '...'] for r in results])


def query_5_3_babysitter_work_hours(session):
    print(f"5.3 SELECT: Babysitter work hours")

    results = session.query(Job.job_id, Job.required_caregiving_type, Job.other_requirements) \
        .filter(Job.required_caregiving_type == 'babysitter').all()

    print_results(['Job ID', 'Type', 'Requirements'],
                  [[r[0], r[1], r[2][:70] + '...'] for r in results])


def query_5_4_elderly_care_astana_no_pets(session):
    print(f"5.4 SELECT: Elderly Care in Astana with 'No pets'")

    results = session.query(User.user_id, User.given_name, User.surname, User.city,
                            Member.house_rules, Job.required_caregiving_type) \
        .join(Member, User.user_id == Member.member_user_id) \
        .join(Job, Member.member_user_id == Job.member_user_id) \
        .filter(and_(User.city == 'Astana',
                     Job.required_caregiving_type == 'elderly_care',
                     Member.house_rules.like('%No pets%'))) \
        .distinct().all()

    print_results(['ID', 'Name', 'City', 'House Rules', 'Seeking'],
                  [[r[0], f"{r[1]} {r[2]}", r[3], r[4][:50] + '...', r[5]] for r in results])



# 6. COMPLEX QUERIES
def query_6_1_applicants_per_job(session):
    print(f"6.1 COMPLEX: Applicants per job (JOIN + Aggregation)")

    results = session.query(Job.job_id,
                            func.concat(User.given_name, ' ', User.surname).label('member'),
                            Job.required_caregiving_type,
                            func.count(JobApplication.caregiver_user_id).label('applicants')) \
        .join(Member, Job.member_user_id == Member.member_user_id) \
        .join(User, Member.member_user_id == User.user_id) \
        .outerjoin(JobApplication, Job.job_id == JobApplication.job_id) \
        .group_by(Job.job_id, User.given_name, User.surname, Job.required_caregiving_type) \
        .order_by(func.count(JobApplication.caregiver_user_id).desc()).all()

    print_results(['Job ID', 'Posted By', 'Type', 'Applicants'], results)


def query_6_2_total_hours_by_caregivers(session):
    print(f"6.2 COMPLEX: Total hours by caregivers")

    results = session.query(Caregiver.caregiver_user_id,
                            func.concat(User.given_name, ' ', User.surname).label('name'),
                            Caregiver.caregiving_type,
                            func.sum(Appointment.work_hours).label('total_hours')) \
        .join(User, Caregiver.caregiver_user_id == User.user_id) \
        .join(Appointment, Caregiver.caregiver_user_id == Appointment.caregiver_user_id) \
        .filter(or_(Appointment.status == 'confirmed', Appointment.status == 'completed')) \
        .group_by(Caregiver.caregiver_user_id, User.given_name, User.surname, Caregiver.caregiving_type) \
        .order_by(func.sum(Appointment.work_hours).desc()).all()

    print_results(['ID', 'Name', 'Type', 'Total Hours'],
                  [[r[0], r[1], r[2], f"{float(r[3]):.2f}"] for r in results])


def query_6_3_average_pay_by_caregiver(session):
    print(f"6.3 COMPLEX: Average pay per caregiver")

    results = session.query(Caregiver.caregiver_user_id,
                            func.concat(User.given_name, ' ', User.surname).label('name'),
                            Caregiver.hourly_rate,
                            func.avg(Caregiver.hourly_rate * Appointment.work_hours).label('avg_pay')) \
        .join(User, Caregiver.caregiver_user_id == User.user_id) \
        .join(Appointment, Caregiver.caregiver_user_id == Appointment.caregiver_user_id) \
        .filter(or_(Appointment.status == 'confirmed', Appointment.status == 'completed')) \
        .group_by(Caregiver.caregiver_user_id, User.given_name, User.surname, Caregiver.hourly_rate) \
        .order_by(func.avg(Caregiver.hourly_rate * Appointment.work_hours).desc()).all()

    print_results(['ID', 'Name', 'Rate', 'Avg Pay/Appointment'],
                  [[r[0], r[1], f"${float(r[2]):.2f}", f"${float(r[3]):.2f}"] for r in results])


def query_6_4_caregivers_earning_above_average(session):
    print(f"6.4 COMPLEX: Caregivers earning above average (Nested)")

    avg_earnings = session.query(func.avg(Caregiver.hourly_rate * Appointment.work_hours)) \
        .join(Appointment, Caregiver.caregiver_user_id == Appointment.caregiver_user_id) \
        .filter(or_(Appointment.status == 'confirmed', Appointment.status == 'completed')) \
        .scalar()

    print(f"\nOverall average: ${float(avg_earnings):.2f}")

    avg_subq = session.query(func.avg(Caregiver.hourly_rate * Appointment.work_hours)) \
        .join(Appointment, Caregiver.caregiver_user_id == Appointment.caregiver_user_id) \
        .filter(or_(Appointment.status == 'confirmed', Appointment.status == 'completed')) \
        .scalar_subquery()

    results = session.query(Caregiver.caregiver_user_id,
                            func.concat(User.given_name, ' ', User.surname).label('name'),
                            Caregiver.hourly_rate,
                            func.sum(Caregiver.hourly_rate * Appointment.work_hours).label('total')) \
        .join(User, Caregiver.caregiver_user_id == User.user_id) \
        .join(Appointment, Caregiver.caregiver_user_id == Appointment.caregiver_user_id) \
        .filter(or_(Appointment.status == 'confirmed', Appointment.status == 'completed')) \
        .group_by(Caregiver.caregiver_user_id, User.given_name, User.surname, Caregiver.hourly_rate) \
        .having(func.sum(Caregiver.hourly_rate * Appointment.work_hours) > avg_subq) \
        .order_by(func.sum(Caregiver.hourly_rate * Appointment.work_hours).desc()).all()

    print_results(['ID', 'Name', 'Rate', 'Total Earnings'],
                  [[r[0], r[1], f"${float(r[2]):.2f}", f"${float(r[3]):.2f}"] for r in results])


# 7. DERIVED ATTRIBUTE

def query_7_total_cost_for_appointments(session):
    print(f"7. DERIVED ATTRIBUTE: Total cost per appointment")

    results = session.query(Appointment.appointment_id,
                            func.concat(User.given_name, ' ', User.surname).label('caregiver'),
                            Caregiver.hourly_rate,
                            Appointment.work_hours,
                            (Caregiver.hourly_rate * Appointment.work_hours).label('total_cost'),
                            Appointment.status) \
        .join(Caregiver, Appointment.caregiver_user_id == Caregiver.caregiver_user_id) \
        .join(User, Caregiver.caregiver_user_id == User.user_id) \
        .filter(or_(Appointment.status == 'confirmed', Appointment.status == 'completed')) \
        .order_by(Appointment.appointment_id).all()

    print_results(['ID', 'Caregiver', 'Rate', 'Hours', 'Total Cost', 'Status'],
                  [[r[0], r[1], f"${float(r[2]):.2f}", f"{float(r[3]):.2f}h",
                    f"${float(r[4]):.2f}", r[5]] for r in results])

    grand_total = sum([float(r[4]) for r in results])
    print(f"\nGrand Total: ${grand_total:.2f}")


# 8. VIEW OPERATION

def query_8_view_job_applications(session):
    print(f"8. VIEW: Job applications with applicant details")

    results = session.execute(text("""
        SELECT ja.job_id, j.required_caregiving_type,
               um.given_name || ' ' || um.surname AS posted_by,
               ja.caregiver_user_id,
               uc.given_name || ' ' || uc.surname AS applicant,
               c.caregiving_type, c.hourly_rate, ja.date_applied
        FROM job_applications ja
        JOIN jobs j ON ja.job_id = j.job_id
        JOIN members m ON j.member_user_id = m.member_user_id
        JOIN users um ON m.member_user_id = um.user_id
        JOIN caregivers c ON ja.caregiver_user_id = c.caregiver_user_id
        JOIN users uc ON c.caregiver_user_id = uc.user_id
        ORDER BY ja.job_id, ja.date_applied
    """)).fetchall()

    print_results(['Job', 'Type', 'Posted By', 'Applicant ID', 'Applicant', 'Specialty', 'Rate', 'Applied'],
                  [[r[0], r[1], r[2], r[3], r[4], r[5], f"${float(r[6]):.2f}", r[7]] for r in results])

    print(f"\nSummary: {len(results)} applications, {len(set([r[0] for r in results]))} unique jobs")


# RUN ALL

def run_all_queries(session):
    print("PART 2: DATABASE QUERIES - CSCI 341 Assignment 3")

    print("3. UPDATE Statements")
    update_3_1_phone_number(session)
    update_3_2_commission_fee(session)

    print("4. DELETE Statements")
    delete_4_1_jobs_by_amina(session)
    delete_4_2_members_on_kabanbay_batyr(session)

    print("5. SIMPLE Queries")
    query_5_1_accepted_appointments(session)
    query_5_2_jobs_with_soft_spoken(session)
    query_5_3_babysitter_work_hours(session)
    query_5_4_elderly_care_astana_no_pets(session)

    print("6. COMPLEX Queries")
    query_6_1_applicants_per_job(session)
    query_6_2_total_hours_by_caregivers(session)
    query_6_3_average_pay_by_caregiver(session)
    query_6_4_caregivers_earning_above_average(session)

    print("7. DERIVED Attribute")
    query_7_total_cost_for_appointments(session)

    print("8. VIEW Operation")
    query_8_view_job_applications(session)

    print("All Queries Completed")