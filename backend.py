from flask import Flask, jsonify, request, Blueprint
from db import mensajes
import uuid
from marshmallow import Schema, fields, validate
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from users_db import usuarios
from users import user_bp
from mensajes import mensajes_bp


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "hola" 
jwt = JWTManager(app)

app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(mensajes_bp, url_prefix="/mensajes")

if __name__ == '__main__':
    app.run(debug=True)
