from flask import Flask, jsonify, request, Blueprint
from db import mensajes
import uuid
from marshmallow import Schema, fields, validate
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from users_db import usuarios
user_bp = Blueprint("users", __name__)

   
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if usuarios[data["usuario"]] == data["contrasena"]:
        acces_token = create_access_token(identity=usuarios)
        return jsonify({"token": acces_token}), 200
    return jsonify({'error': 'User not found'}), 404
    
@user_bp.route("/users", methods=["GET"])
def obtener_usuarios():
    return jsonify(usuarios), 200

@user_bp.route("/register", methods=["POST"])
def registrar_usuario():
    data = request.get_json()
    if not data or 'usuario' not in data or "contrasena" not in data:
        return jsonify({'error': 'Missing message'}), 400
    usuarios[data["usuario"]] = data["contrasena"]
    return jsonify({'Mensaje': 'User registered'}), 200  