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
from models import db, User, Planet, Character, Favourite_Character, Favourite_Planet
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
app.config["JWT_SECRET_KEY"] = "ha82hbk50gjqva978bru3ifeid20al0l9j2ks8d4kd72dncjafqw093jb8c0zz1"
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/signup', methods=['POST'])
def signup_post():
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object.", status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email.', status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password.', status_code=400)

    user = User.query.filter_by(email = body['email']).first()
    if user:
        raise APIException('There is already an account with this email.', status_code=400)

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=body['email'], password=bcrypt.generate_password_hash(body['password']).decode('utf-8'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return "ok", 200

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    user = User.query.filter_by(email = email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        raise APIException('Please check your login details and try again.', status_code=400)

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

@app.route('/users', methods=['GET'])
def handle_users():
    query = User.query.all()
    users = list(map(lambda x: x.serialize(), query))
    return jsonify(users), 200

@app.route('/planets', methods=['GET'])
def handle_planets():
    query = Planet.query.all()
    planets = list(map(lambda x: x.serialize(), query))
    return jsonify(planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet_by_id(planet_id):
    query = Planet.query.get(planet_id)
    if not query:
        raise APIException('Planet not found.', status_code=404)

    return jsonify(query.serialize()), 200

@app.route('/planets', methods=['POST'])
def handle_planet():
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object.", status_code=400)
    if 'name' not in body:
        raise APIException('You need to specify the name.', status_code=400)
    if 'climate' not in body:
        raise APIException('You need to specify the climate.', status_code=400)
    if 'diameter' not in body:
        raise APIException('You need to specify the diameter.', status_code=400)
    if 'orbital_period' not in body:
        raise APIException('You need to specify the orbital_period.', status_code=400)
    if 'population' not in body:
        raise APIException('You need to specify the population.', status_code=400)

    new_planet = Planet(name=body['name'], climate=body['climate'], diameter=body['diameter'], orbital_period=body['orbital_period'], population=body['population'] )
    db.session.add(new_planet)
    db.session.commit()
    return "ok", 200

@app.route('/favourite_planet', methods=['POST'])
def handle_favourite_planet():
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object.", status_code=400)
    if 'user_id' not in body:
        raise APIException('You need to specify the user_id.', status_code=400)
    if 'planet_id' not in body:
        raise APIException('You need to specify the planet_id.', status_code=400)

    new_favourite = Favourite_Planet(user_id=body['user_id'], planet_id=body['planet_id'] )
    db.session.add(new_favourite)
    db.session.commit()
    return "ok", 200

@app.route('/characters', methods=['GET'])
def handle_characters():
    query = Character.query.all()
    characters = list(map(lambda x: x.serialize(), query))
    return jsonify(characters), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def handle_character_by_id(character_id):
    query = Character.query.get(character_id)
    if not query:
        raise APIException('Character not found.', status_code=404)

    return jsonify(query.serialize()), 200

@app.route('/characters', methods=['POST'])
def handle_character():
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object.", status_code=400)
    if 'name' not in body:
        raise APIException('You need to specify the name.', status_code=400)
    if 'birth_year' not in body:
        raise APIException('You need to specify the birth_year.', status_code=400)
    if 'height' not in body:
        raise APIException('You need to specify the height.', status_code=400)
    if 'skin_color' not in body:
        raise APIException('You need to specify the skin_color.', status_code=400)
    if 'eye_color' not in body:
        raise APIException('You need to specify the eye_color.', status_code=400)

    new_character = Character(name=body['name'], birth_year=body['birth_year'], height=body['height'], skin_color=body['skin_color'], eye_color=body['eye_color'] )
    db.session.add(new_character)
    db.session.commit()
    return "ok", 200

@app.route('/favourites', methods=['GET'])
def handle_favourites():
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object.", status_code=400)
    if 'user_id' not in body:
        raise APIException('You need to specify the user_id.', status_code=400)

    id = body['user_id']

    query_planets = Favourite_Planet.query.filter(Favourite_Planet.user_id == id).all()
    query_characters = Favourite_Character.query.filter(Favourite_Character.user_id == id).all()
    
    planets = list(map(lambda x: x.serialize(), query_planets))
    characters = list(map(lambda x: x.serialize(), query_characters))

    return jsonify({"characters": characters, "planets": planets}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
