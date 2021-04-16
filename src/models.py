from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)


class Planets(db.Model):
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    population = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    diameter = db.Column(db.Integer)
    climate = db.Column(db.String(40))
    gravity = db.Column(db.String(40))
    terrain = db.Column(db.String(40))
    surface_water = db.Column(db.Integer)
    gravity = db.Column(db.String(40))
    

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }