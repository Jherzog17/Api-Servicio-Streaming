from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate, ValidationError

from users_bp import users_db
from historial_db import historial
from media_db import medios

historial_bp = Blueprint("historial", __name__)

class HistorialItemSchema(Schema):
    id_medio_de_streaming = fields.Int(required=True)
    fecha_visualizacion = fields.Date(required=False)

@historial_bp.route("/usuarios/<id_usuario>/historial", methods=["GET"])
@jwt_required()
def consultar_historial(id_usuario):
    current_user = get_jwt_identity()
    if current_user != id_usuario:
        return jsonify({"error": "No autorizado para ver este historial"}), 403
    
    # usuario existe ¿
    if id_usuario not in users_db:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    # hisorial y si no hay lista vacia
    lista_historial = historial.get(id_usuario, [])
    return jsonify({"historial": lista_historial}), 200

@historial_bp.route("/usuarios/<id_usuario>/historial", methods=["POST"])
@jwt_required()
def anadir_al_historial(id_usuario):
    current_user = get_jwt_identity()
    if current_user != id_usuario:
        return jsonify({"error": "No autorizado para modificar este historial"}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON'}), 400
    try:
        schema = HistorialItemSchema()
        schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # el medio existe ?
    if data['id_medio_de_streaming'] not in medios:
        return jsonify({'error': 'El medio de streaming no existe'}), 404

    if id_usuario not in users_db:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    # si no hay historial rntonces se crea la lista 
    if id_usuario not in historial:
        historial[id_usuario] = []
    # + itm a la lista
    historial[id_usuario].append(data)
    
    return jsonify({"mensaje": "Añadido al historial", "historial": historial[id_usuario]}), 201