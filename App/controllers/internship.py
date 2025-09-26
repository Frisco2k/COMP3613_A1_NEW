from App.database import db
from App.models.internship import Internships, Shortlist
from App.models.employer import Employer
from App.models.student import Student
from App.models.staff import Staff


def create_position(employer, title, desc):
    p = Internships(
        title=title.strip(),
        description=(desc or "").strip(),
        employer_id=employer.id
    )
    db.session.add(p)
    db.session.commit()
    return p

def get_position(position_id):
    return Internships.query.get(position_id)

def list_positions():
    return Internships.query.order_by(Internships.id.desc()).all()

def list_positions_for_employer(emp):
    return Internships.query.filter_by(employer_id=emp.id).order_by(Internships.id.desc()).all()


def shortlist_add(staff, student, position):
    entry = Shortlist(
        student_id=student.id,
        position_id=position.id,
        staff_supervisor_id=staff.id,
        status="PENDING",
    )
    db.session.add(entry)
    db.session.commit()
    return entry

def shortlist_for_position(position_id):
    return Shortlist.query.filter_by(position_id=position_id).all()

def shortlist_set_status(entry, status):
    if status not in ("PENDING", "ACCEPTED", "REJECTED"):
        print("status must be PENDING, ACCEPTED, or REJECTED")
    entry.status = status
    db.session.commit()
    return entry

def student_shortlists(student):
    return Shortlist.query.filter_by(student_id=student.id).all()
