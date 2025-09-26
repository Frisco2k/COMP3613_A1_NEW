from App.database import db
from .employer import Employer
from .student import Student
from .staff import Staff

class Internships(db.Model):
    __tablename__ = "internships"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    employer_id = db.Column(db.Integer, db.ForeignKey(Employer.id), nullable=False)
    employer = db.relationship(Employer, lazy="joined")

    def __repr__(self):
        return f"<Position #{self.id} {self.title} @ {self.employer.company}>"

class Shortlist(db.Model):
    __tablename__ = "shortlist"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey(Internships.id), nullable=False)
    staff_supervisor_id = db.Column(db.Integer, db.ForeignKey(Staff.id), nullable=False)

    status = db.Column(db.String(20), default="PENDING", nullable=False)

    student = db.relationship(Student, lazy="joined", foreign_keys=[student_id])
    position = db.relationship(Internships, lazy="joined", foreign_keys=[position_id])
    added_by_staff = db.relationship(Staff, lazy="joined", foreign_keys=[staff_supervisor_id])

    __table_args__ = (
        db.UniqueConstraint("student_id", "position_id", name="uq_student_position"),
    )

    def __repr__(self):
        return f"<Shortlist #{self.id} {self.student.name} -> {self.position.title} [{self.status}]>"
