from App.database import db

class Employer(db.Model):
    __tablename__ = "employers"
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(160), unique=True, nullable=False)

    def __repr__(self):
        return f"<Employer #{self.id} {self.company}>"