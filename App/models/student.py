from App.database import db

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False, unique = True)

    def __repr__(self):
        return f"<Student #{self.id} {self.name}>"
