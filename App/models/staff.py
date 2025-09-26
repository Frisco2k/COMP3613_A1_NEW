from App.database import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), primary_key = False, nullable = False, unique = True)

    def __repr__(self):
        return f"<Staff #{self.id} {self.name}>"


