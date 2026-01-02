from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import JWTManager
from users_bp import users_bp
from media_bp import media_bp
from historial_bp import historial_bp
from suscripciones_bp import suscripciones_bp
import os

app = Flask(__name__)
#Si no tienes la clave secreta como variable de entorno descomentar la siguiente y comentar la de dos despues
#app.config["JWT_SECRET_KEY"] = "hola"
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

app.register_blueprint(users_bp, url_prefix="/usuarios")
app.register_blueprint(media_bp, url_prefix="/medio_de_streaming")
app.register_blueprint(historial_bp)
app.register_blueprint(suscripciones_bp)

if __name__ == "__main__":
    app.run(debug=True)