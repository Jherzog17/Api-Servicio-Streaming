from flask import Flask, jsonify, request, Blueprint
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime
from media_db import medios

media_bp = Blueprint("medio_de_streaming", __name__)

class MediaSchema(Schema):
    id_medio_de_streaming=fields.Int(required=True)
    pais=fields.Str(required=True)
    fecha_de_subida=fields.Date(required=True)

@media_bp.route("/<int:id_medio_de_streaming>", methods=["GET"])
def reproducir_medio_de_streaming(id_medio_de_streaming):
    data=medios.get(id_medio_de_streaming)
    if not data:
        return jsonify({'error':'Medio not found'}), 404
    return jsonify({"medio_de_streaming":data}),200

@media_bp.route("/", methods=["GET"])
def listar_medios():
    pais = request.args.get("pais")
    fecha_subida = request.args.get("fecha_subida")
    num_items = request.args.get("num_items")
    
    # Filtrar por país si se ha introducido como parámetro
    if pais:
        data = []
        for id_medio, medio in medios.items():
            if str(medio.get("pais", "")).lower() == str(pais).lower():
                data.append({"id_medio_de_streaming": id_medio, "medio": medio})
        if not data:
            return jsonify({'error': 'No hay medios de streaming en ese país'}), 404
        return jsonify({"medio_de_streaming": data}), 200
    
    # Filtrar por fecha de subida (con límite opcional)
    if fecha_subida:
        data = []
        for id_medio, medio in medios.items():
            if str(medio.get("fecha_de_subida", "")).lower() == str(fecha_subida).lower():
                data.append({"id_medio_de_streaming": id_medio, "medio": medio})
        if not data:
            return jsonify({'error': 'No hay medios de streaming con esa fecha de subida'}), 404
        # Aplicar límite si se especifica num_items
        if num_items:
            try:
                num_items = int(num_items)
                data = data[:num_items]
            except ValueError:
                return jsonify({"Error": "num_items debe ser entero"}), 400
        return jsonify({'medio_de_streaming': data}), 200
    
    # Caso de que no haya filtro
    return jsonify(medios), 200

@media_bp.route("/anadir_medio", methods=["POST"])
def anadir_medio():
    data=request.get_json()
    if not data:
        return jsonify({"Error": "JSON vacío"}), 400
    try:
        schema=MediaSchema()
        schema.load(data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 409
    
    medios[data["id_medio_de_streaming"]]={"pais": data["pais"], "fecha_de_subida": str(data["fecha_de_subida"])}
    return jsonify({"Mensaje": "Medio de streaming añadido"}), 201

@media_bp.route("/<string:id_medio_de_streaming>", methods=["DELETE"])
def eliminar_medio(id_medio_de_streaming):
    id_medio=medios.get(id_medio_de_streaming)
    if id_medio is not None:
        del medios[id_medio_de_streaming]
        return jsonify({"Mensaje": "Medio de streaming eliminado"}), 200
    else:
        return jsonify({"Error": "Medio no encontrado"}), 404

@media_bp.route("/<string:id_medio_de_streaming>", methods=["PUT"])
def editar_medio(id_medio_de_streaming):
    data=request.get_json()
    id_medio=medios.get(id_medio_de_streaming)
    if id_medio is None: 
        return jsonify({"Error": "Medio de streaming no encontrado"}), 404
    if not data:
        return jsonify({"Error": "JSON vacio"}), 400
    try:
        schema=MediaSchema()
        schema.load(data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 409
    medios[id_medio_de_streaming]={"pais": data["pais"], "fecha_de_subida":str(data["fecha_de_subida"])}
    return jsonify({"mensaje": "Medio de streaming editado"}), 200