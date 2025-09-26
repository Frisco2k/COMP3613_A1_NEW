from App.database import db
from App.models.student import Student
from App.models.staff import Staff
from App.models.employer import Employer
from sqlalchemy.exc import IntegrityError


def create_student(name):
    existing = Student.query.filter_by(name=name).first()
    if existing:
        print(f"Error: Student with name '{name}' already exists (id={existing.id}).")
        return None
    s = Student(name=name)
    db.session.add(s)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print(f"Error: Could not create student '{name}'. Name must be unique.")
        return None
    return s

def create_staff(name):
    existing = Staff.query.filter_by(name=name).first()
    if existing:
        print(f"Error: Staff with name '{name}' already exists (id={existing.id}).")
        return None
    s = Staff(name=name)
    db.session.add(s)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print(f"Error: Could not create staff '{name}'. Name must be unique.")
        return None
    return s

def create_employer(company):
    existing = Employer.query.filter_by(company=company).first()
    if existing:
        print(f"Error: Employer with company '{company}' already exists (id={existing.id}).")
        return None
    e = Employer(company=company)
    db.session.add(e)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print(f"Error: Could not create employer '{company}'. Company must be unique.")
        return None
    return e


def get_student(name):
    return Student.query.filter_by(name=name.strip()).first()

def get_staff(name):
    return Staff.query.filter_by(name=name.strip()).first()

def get_staff_by_id(staff_id):
    return Staff.query.get(staff_id)

def get_employer(company):
    return Employer.query.filter_by(company=company.strip()).first()

def list_students():
    return Student.query.order_by(Student.name.asc()).all()

def list_staff():
    return Staff.query.order_by(Staff.name.asc()).all()

def list_employers():
    return Employer.query.order_by(Employer.company.asc()).all()
