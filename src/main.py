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
from models import db, User, Planet, Character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

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

@app.route('/planets', methods=['POST'])
def handle_planet():
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'name' not in body:
        raise APIException('You need to specify the name', status_code=400)
    if 'climate' not in body:
        raise APIException('You need to specify the climate', status_code=400)
    if 'diameter' not in body:
        raise APIException('You need to specify the diameter', status_code=400)
    if 'orbital_period' not in body:
        raise APIException('You need to specify the orbital_period', status_code=400)
    if 'population' not in body:
        raise APIException('You need to specify the population', status_code=400)

    new_planet = Planet(name=body['name'], climate=body['climate'], diameter=body['diameter'], orbital_period=body['orbital_period'], population=body['population'] )
    db.session.add(new_planet)
    db.session.commit()
    return "ok", 200

@app.route('/characters', methods=['GET'])
def handle_characters():
    query = Character.query.all()
    characters = list(map(lambda x: x.serialize(), query))
    return jsonify(characters), 200

@app.route('/characters', methods=['POST'])
def handle_character():
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'name' not in body:
        raise APIException('You need to specify the name', status_code=400)
    if 'birth_year' not in body:
        raise APIException('You need to specify the birth_year', status_code=400)
    if 'height' not in body:
        raise APIException('You need to specify the height', status_code=400)
    if 'skin_color' not in body:
        raise APIException('You need to specify the skin_color', status_code=400)
    if 'eye_color' not in body:
        raise APIException('You need to specify the eye_color', status_code=400)

    new_character = Character(name=body['name'], birth_year=body['birth_year'], height=body['height'], skin_color=body['skin_color'], eye_color=body['eye_color'] )
    db.session.add(new_character)
    db.session.commit()
    return "ok", 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
