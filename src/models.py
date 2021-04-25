from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    fav_people = db.relationship("Fav_People", lazy=True)
    fav_planet = db.relationship("Fav_Planet", lazy=True)

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

class Planet(db.Model):
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
    
    def _repr_(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "Name": self.name,
            "Climate": self.climate,
            "Population": self.population,
            "Orbital Period": self.orbital_period,
            "Rotation Period": self.rotation_period,
            "Diameter": self.diameter,
            "Terrain": self.terrain
        }

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
    
    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "Name": self.name,
            "Gender": self.gender,
            "Hair Color": self.hair_color,
            "Eye Color": self.eye_color,
            "Birth Year": self.birth_year,
            "Height": self.height,
            "Skin Color": self.skin_color
        }

class Fav_People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    people = db.relationship("People", lazy="subquery")
    
    def _repr_(self):
        return "<Fav_People %r>" % self.people.name
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "route": "/people/" + str(self.id),
            "name": self.people.name
        }

class Fav_Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    planet = db.relationship("Planet", lazy="subquery")
    
    def _repr_(self):
        return "<Fav_Planet %r>" % self.planet.name
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "route": "/planet/" + str(self.id),
            "name": self.planet.name
        }