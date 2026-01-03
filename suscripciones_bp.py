from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate, ValidationError

from users_bp import users_db
from suscripciones_db import suscripciones

suscripciones_bp = Blueprint("suscripciones", __name__)


class SuscripcionSchema(Schema):
    id_suscripcion=fields.Int(required=True)
    tipo=fields.Str(required=True)
    precio=fields.Str(required=True)

@suscripciones_bp.route("/usuarios/<id_usuario>/suscripciones", methods=["POST"])
@jwt_required()
def pagar_suscripcion(id_usuario):
    current_user = get_jwt_identity()
    id_usuario=str(id_usuario)
    if current_user != id_usuario:
        return jsonify({"error": "No autorizado"}), 403
    
    data=request.get_json()
    if not data:
        return jsonify({'error':'Missing JSON'}), 400
    try:
        schema=SuscripcionSchema()
        schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages),400
    if id_usuario not in users_db:
        return jsonify({'error':'No existe usuario'}), 404
    suscripciones[id_usuario]=data
    return jsonify({"suscripcion":data}),200

@suscripciones_bp.route("/usuarios/<id_usuario>/suscripciones", methods=["PUT"])
@jwt_required()
def modificar_suscripcion(id_usuario):
    current_user = get_jwt_identity()
    id_usuario = str(id_usuario)
    if current_user != id_usuario:
        return jsonify({"error": "No autorizado"}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON'}), 400
    if id_usuario not in users_db:
        return jsonify({'error':'No existe usuario'}), 404
    if id_usuario not in suscripciones:
        return jsonify({'error': 'No existe suscripcion'}), 404
    try:
        schema=SuscripcionSchema()
        schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages),400
    suscripciones[id_usuario] = data
    return jsonify({"suscripcion": data}), 200

@suscripciones_bp.route("/usuarios/<id_usuario>/suscripciones", methods=["DELETE"])
@jwt_required()
def cancelar_suscripcion(id_usuario):
    current_user = get_jwt_identity()
    id_usuario = str(id_usuario)
    if current_user != id_usuario:
        return jsonify({"error": "No autorizado"}), 403
    
    if id_usuario not in users_db:
        return jsonify({'error':'No existe usuario'}), 404
    if id_usuario not in suscripciones:
        return jsonify({'error':'No existe suscripcion'}),404
    del suscripciones[id_usuario]
    return jsonify({'mensaje':'suscripcion cancelada'}),200

@suscripciones_bp.route("/usuarios/<id_usuario>/suscripciones", methods=["GET"])
@jwt_required()
def get_suscripcion(id_usuario):
    current_user = get_jwt_identity()
    if current_user != id_usuario:
        return jsonify({"error": "No autorizado"}), 403
    
    if id_usuario in suscripciones:
        return jsonify({"mensaje":suscripciones[id_usuario]}), 200
    else:
        return jsonify({"Error": "Suscripción no encontrada o usuario no tiene suscripción activa"}),404