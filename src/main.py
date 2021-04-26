"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Fav_Planet, Fav_People
#JWT - SECURITY
#from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import datetime
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200


#register---------------------------------------------------------
@app.route("/register", methods=["POST"])
def register_user():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email is None:
        return jsonify({"msg": "No email was provided"}), 400
    if password is None:
        return jsonify({"msg": "No password was provided"}), 400
    
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        # the user was not found on the database
        return jsonify({"msg": "User already exists"}), 401
    else:
        new_user = User()
        new_user.email = email
        new_user.password = password

        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User created successfully"}), 200
    
#login---------------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        # Validate
        if email is None:
            return jsonify({"error": "Please provide an email"}), 400
        if password is None:
            return jsonify({"error": "Please provide a password"}), 400
        
        user = User.query.filter_by(email=email, password=password).first()

        if user is None:
            return jsonify({"error": "Invalid email or password"}), 401 
        elif user.password != password:
            return jsonify({"error": "User or password not found"}), 401
        else:
            print(user)
            # create a new token with the user id inside
            access_token = create_access_token(identity=user.id)
            return jsonify({ "token": access_token, "user_id": user.id }), 200

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
     # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    print(current_user_id, user)
    return jsonify({"id": user.id, "email": user.email }), 200

# --User--------------------------------------------------------
@app.route('/users', methods=['GET'])
def listarUsuarios():
    users = User.query.all()
    request = list(map(lambda user:user.serialize(),users))    
    return jsonify(request), 200

# @app.route('/favorites/<id>', methods=['GET'])
# def favs_usuario(id):
#     #user = User.query.get(id)
#     # favs = Favorites.query.filter_by(id=id).first()
#     # # if user is None:
#     # #     raise APIException("Message:No se encontro el user",status_code=404)
#     # request = favs.serialize()
#     # return jsonify(request), 200
#     favs = Favorites.query.all()
#     request = list(map(lambda x:x.serialize(),favs))    
#     return jsonify(request), 200

@app.route('/users', methods=["POST"])
def crear_usuarios():
    data = request.get_json()
    #hashed_password = generate_password_hash(data["password"],method='sha256')
    user1 = User(username=data["username"],email=data["email"],password=data["password"])
    db.session.add(user1)
    db.session.commit()
    return jsonify("Message : Se adiciono un usuario!"),200

@app.route('/users/<id>', methods=["DELETE"])
@jwt_required()
def delete_usuarios(id):
    current_user = get_jwt_identity()
    user1 = User.query.get(id)
    if user1 is None:
        raise APIException("usuario no existe!",status_code=404)
    db.session.delete(user1)
    db.session.commit()
    return jsonify({"Proceso realizado con exito por el usuario:" : current_user}),200


# --Planets--------------------------------------------------------
@app.route('/testplanets', methods=['GET'])
def get_planets():
    response = {"message": "it worked"}
    return jsonify(response)

@app.route('/planet', methods=['GET'])
def getPlanets():
    planet = Planet.query.all()
    request = list(map(lambda planet:planet.serialize(),planet))    
    return jsonify(request), 200

@app.route('/planets/<int:id>', methods=['GET'])
def getPlanets_id(id):
    #user = User.query.get(id)
    planeta = Planet.query.filter_by(id=id).first()
    if planeta is None:
        raise APIException("Message:Requested data not found",status_code=404)
    request = planeta.serialize()
    return jsonify(request), 200

# --People--------------------------------------------------------
@app.route('/testpeople/', methods=['GET'])
def get_people():
    response = {"message": "it worked"}
    return jsonify(response)

@app.route('/people', methods=['GET'])
def getPeople():
    people = People.query.all()
    request = list(map(lambda people:people.serialize(),people))    
    return jsonify(request), 200

@app.route('/people/<int:id>', methods=['GET'])
def getPeople_id(id):
    #user = User.query.get(id)
    people = People.query.filter_by(id=id).first()
    if people is None:
        raise APIException("Message:Requested data not found",status_code=404)
    request = people.serialize()
    return jsonify(request), 200

# --Favorites--------------------------------------------------------
@app.route('/favorites/', methods=['GET'])
def get_favorites():
    response = {"message": "it worked"}
    return jsonify(response)

# @app.route('/favorites/<int:user_id>', methods=['GET'])
# def get_favorites_id(user_id):
#     # user_id=3
#     todos = Favorites.query.all()
#     lista_favs = list(map(lambda x: x.serialize(), todos))
#     user_favs = list(filter( lambda x: x["user_id"] == user_id , lista_favs))
#     favoritos = list(map( lambda x: x["fav_name"], user_favs))
#     result = favoritos

#     return jsonify(result), 200

@app.route('/users/<int:id_user>/favorites', methods=['GET'])
def get_favoritesfromuser(id_user):
    favpeople = Fav_People.query.filter_by(user_id=id_user)
    favplanet = Fav_Planet.query.filter_by(user_id=id_user)
    favpeople_serialize = list(map(lambda x:x.serialize(),favpeople))
    favplanet_serialize = list(map(lambda x:x.serialize(),favplanet))
    fav_response = favpeople_serialize + favplanet_serialize
    return jsonify(fav_response)

@app.route('/users/<int:id_user>/favorites', methods=['POST'])
# @jwt_required()
def POST_favoritestouser(id_user):
    tipo = request.json.get("tipo", None)
    id = request.json.get("id", None)
    
    if tipo == "planet":
        favPlanet = Fav_Planet(user_id=id_user, planet_id=id)
        db.session.add(favPlanet)
        db.session.commit()
        
        return jsonify(favPlanet.serialize()), 200
    
    if tipo == "people":
        favPeople = Fav_People(user_id=id_user, people_id=id)
        db.session.add(favPeople)
        db.session.commit()
        
        return jsonify(favPeople.serialize()), 200
    return APIException("Bad Request", status_code=400)

@app.route('/favorite/<string:tipo>/<int:favorite_id>', methods=['DELETE'])
# @jwt_required()
def delete_favfromuser(tipo, favorite_id):
    if tipo == "planet":
        delete_fav = Fav_Planet.query.filter_by(id=favorite_id).first()
        print(delete_fav)
        if delete_fav is None:
            return "Not Found", 401
        else:
            db.session.delete(delete_fav)
            db.session.commit()
            return jsonify(delete_fav.serialize()),200
    elif tipo == "people":
        delete_fav = Fav_People.query.filter_by(id=favorite_id).first()
        print(delete_fav)
        if delete_fav is None:
            return "Not Found", 401
        else:
            db.session.delete(delete_fav)
            db.session.commit()
            return jsonify(delete_fav.serialize()),200
        
    return "Wrong Request", 402


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
