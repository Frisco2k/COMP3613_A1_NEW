from flask import Flask
from App.database import db
from App.models.student import Student
from App.models.staff import Staff
from App.models.employer import Employer
from App.models.internship import Internships, Shortlist

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

import click
from flask.cli import with_appcontext

from App.controllers.user import (
    create_student, create_staff, create_employer,
    get_student, get_staff_by_id, get_employer,
    list_students, list_staff, list_employers,
)
from App.controllers.internship import (
    create_position, get_position, list_positions, list_positions_for_employer,
    shortlist_add, shortlist_for_position, shortlist_set_status, student_shortlists
)
from App.models.internship import Shortlist

def filter_student(name):
    s = get_student(name)
    if not s:
        print("Error: Student '" + name + "' not found.")
        return None
    return s

def filter_staff_by_id(staff_id):
    s = get_staff_by_id(staff_id)
    if not s:
        print("Error: Staff id " + str(staff_id) + " not found.")
        return None
    return s

def filter_employer(company):
    e = get_employer(company)
    if not e:
        print("Error: Employer '" + company + "' not found.")
        return None
    return e

def filter_position(pid):
    p = get_position(pid)
    if not p:
        print("Error: Position #" + str(pid) + " not found.")
        return None
    return p

@app.cli.command("init-db")
@with_appcontext
def init_db_cmd():
    db.create_all()

    bob = create_staff("Bob")
    rob = create_staff("Rob")

    alice = create_student("Alice")
    erina = create_student("Erina")

    totsuki = create_employer("Totsuki Culinary Academy")
    central = create_employer("Central Inc.")

    p1 = create_position(totsuki, "Web Development Intern", "Work on Cooking Web Apps")
    p2 = create_position(central, "Data Analyst Intern", "Assist in analytics")

    print("Seeded initial data:")
    print(f" Staff: {bob.name} (id={bob.id}), {rob.name} (id={rob.id})")
    print(f" Students: {alice.name} (id={alice.id}), {erina.name} (id={erina.id})")
    print(f" Employers: {totsuki.company} (id={totsuki.id}), {central.company} (id={central.id})")
    print(f" Positions: {p1.title} @ {totsuki.company} (id={p1.id}), {p2.title} @ {central.company} (id={p2.id})")
    print("DB initialized and initial entities created.")

@app.cli.command("reset-db")
@with_appcontext
def reset_db_cmd():
    db.drop_all()
    db.create_all()
    print("DB reset (dropped & created).")

@app.cli.group("student")
def student_group():
    """Student actions."""
    pass

@student_group.command("create")
@click.argument("name")
@with_appcontext
def student_create(name):
    s = create_student(name)
    if not s:
        return
    print(f"Created student #{s.id} {s.name}")

@student_group.command("my-shortlists")
@click.argument("student_name")
@with_appcontext
def student_my_shortlists(student_name):
    std = filter_student(student_name)
    if not std:
        return
    result = student_shortlists(std)
    if not result:
        print("No shortlist entries.")
        return
    for e in result:
        print(f"[{e.status}] entry #{e.id} -> '{e.position.title}' @ {e.position.employer.company}")

@app.cli.group("staff")
def staff_group():
    """Staff actions."""
    pass

@staff_group.command("create")
@click.argument("name")
@with_appcontext
def staff_create(name):
    s = create_staff(name)
    if not s:
        return
    print(f"Created staff #{s.id} {s.name}")

@staff_group.command("list")
@with_appcontext
def staff_list_cmd():
    result = list_staff()
    if not result:
        print("No staff.")
        return
    for s in result:
        print(f"Staff #{s.id} {s.name}")

@staff_group.command("shortlist-add")
@click.argument("staff_id", type=int)
@click.argument("student")
@click.argument("position_id", type=int)
@with_appcontext
def staff_shortlist_add(staff_id, student, position_id):
    stf = filter_staff_by_id(staff_id)
    if not stf:
        return
    std = filter_student(student)
    if not std:
        return
    pos = filter_position(position_id)
    if not pos:
        return
    e = shortlist_add(stf, std, pos)
    print(f"Shortlisted {std.name} for '{pos.title}' (entry #{e.id}) by Staff #{stf.id} {stf.name}")

@app.cli.group("employer")
def employer_group():
    """Employer actions."""
    pass

@employer_group.command("create")
@click.argument("company")
@with_appcontext
def employer_create_company(company):
    e = create_employer(company)
    if not e:
        return
    print(f"Created employer #{e.id} {e.company}")

@employer_group.command("create-position")
@click.argument("company")
@click.argument("title")
@click.argument("description", required=False, default="")
@with_appcontext
def employer_create(company, title, description):
    emp = filter_employer(company)
    p = create_position(emp, title, description or "")
    print(f"Position #{p.id} '{p.title}' @ {emp.company}")

@employer_group.command("list")
@click.argument("company", required=False)
@with_appcontext
def employer_list(company):
    result = list_positions_for_employer(filter_employer(company)) if company else list_positions()
    if not result:
        print("No positions.")
        return
    for p in result:
        print(f"<Pos {p.id}> {p.title} @ {p.employer.company}")

@employer_group.command("shortlist")
@click.argument("company")
@click.argument("position_id", type=int)
@with_appcontext
def employer_shortlist(company, position_id):
    emp = filter_employer(company)
    if not emp:
        return
    pos = filter_position(position_id)
    if not pos:
        return
    if pos.employer_id != emp.id:
        print("That position does not belong to this company.")
        return
    result = shortlist_for_position(position_id)
    if not result:
        print("No students shortlisted for this position.")
        return
    print(f"Shortlist for <Pos {pos.id}> {pos.title} @ {emp.company}:")
    for e in result:
        print(f"  [{e.status}] entry #{e.id} - {e.student.name} (added by {e.added_by_staff.name})")

@employer_group.command("accept")
@click.argument("company")
@click.argument("shortlist_id", type=int)
@with_appcontext
def employer_accept(company, shortlist_id):
    emp = filter_employer(company)
    if not emp:
        return
    e = Shortlist.query.get(shortlist_id)
    if not e:
        print("Shortlist entry not found.")
        return
    if e.position.employer_id != emp.id:
        print("This shortlist is not for a position owned by that company.")
        return 
    shortlist_set_status(e, "ACCEPTED")
    print(f"Accepted {e.student.name} for '{e.position.title}' @ {emp.company}")

@employer_group.command("reject")
@click.argument("company")
@click.argument("shortlist_id", type=int)
@with_appcontext
def employer_reject(company, shortlist_id):
    emp = filter_employer(company)
    if not emp:
        return
    e = Shortlist.query.get(shortlist_id)
    if not e:
        print("Shortlist entry not found.")
        return
    if e.position.employer_id != emp.id:
        print("This shortlist is not for a position owned by that company.")
        return  
    shortlist_set_status(e, "REJECTED")
    print(f"Rejected {e.student.name} for '{e.position.title}' @ {emp.company}")