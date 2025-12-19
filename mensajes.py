
from flask import Flask, jsonify, request, Blueprint
from db import mensajes
import uuid
from marshmallow import Schema, fields, validate
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from users_db import usuarios
mensajes_bp = Blueprint("mensajes", __name__)

class MensajeSchema(Schema):
    id = fields.UUID()
    message = fields.Str()

@mensajes_bp.route('/send', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Missing message'}), 400
    new_id = uuid.uuid4().hex
    data["id"] = new_id
    #Comprobar que data usa el esquema adecuado
    try:
        schema = MensajeSchema()
        schema.load(data)
    except Exception as e:
        return jsonify(e.messages), 400

    mensajes[f"Mensaje {len(mensajes)+1}"] = data
    return jsonify({'Mensaje': data["message"]}), 200

@mensajes_bp.route('/messages', methods=['GET'])
def obtener_mensajes():
    return jsonify(mensajes), 200

@mensajes_bp.route("/modify", methods=['PUT'])
def modificar_mensaje():
    data = request.get_json()
    if not data or 'id' not in data:
        return jsonify({'error': 'Missing message'}), 400
    id = data["id"]
    for key,value in mensajes.items():
        if value["id"] == id:
            value["message"] = data["message"]
            try:
                schema = MensajeSchema()
                schema.load(value)
            except Exception as e:
                return jsonify(e.messages), 400
            return jsonify({'Mensaje': value}), 200
    return jsonify({'error': 'Message not found'}), 404

@mensajes_bp.route("/delete", methods=['DELETE'])
def eliminar_mensaje():
    data = request.get_json()
    id = data["id"]
    for key, value in mensajes.items():
        if value["id"] == id:
            del mensajes[key]
            return jsonify({'Mensaje': 'Item deleted'}), 200
    return jsonify({'error': 'Message not found'}), 404
   
