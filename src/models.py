from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password #para efectos de estudiar, si quiero verlo, pero real life NOOOOO se pone
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    climate = db.Column(db.String(40))
    population = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    diameter = db.Column(db.Integer)
    terrain = db.Column(db.String(40))

class People(db.Model):
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(15))
    hair_color = db.Column(db.String(40))
    eye_color = db.Column(db.String(40))
    birth_year = db.Column(db.String(40), nullable=False)
    height = db.Column(db.Integer)
    skin_color = db.Column(db.String(40))

class Vehicles(db.Model):
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(50))
    cargo_capacity = db.Column(db.Integer)
    vehicle_class = db.Column(db.String(40))
    length = db.Column(db.Integer)
    crew = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    consumables = db.Column(db.String(40))
    

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    fav_name = db.Column(db.String(250), nullable=False)
    
    def _repr_(self):
        return "<Favorites %r>" % self.id
    
    def serialize_favorites(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "fav_name": self.fav_name
        }
