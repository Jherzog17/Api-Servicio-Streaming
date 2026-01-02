from flask import Flask, jsonify, request, Blueprint
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime
from media_db import medios

media_bp = Blueprint("medio_de_streaming", __name__)

class MediaSchema(Schema):
    id_medio_de_streaming=fields.Int(required=True)
    pais=fields.Str(required=True)
    fecha_de_subida=fields.Date(required=True)

@media_bp.route("/<string:id_medio_de_streaming>", methods=["GET"])
def reproducir_medio_de_streaming(id_medio_de_streaming):
    data=medios.get(id_medio_de_streaming)
    if not data:
        return jsonify({'error':'Medio not found'}), 404
    return jsonify({"medio_de_streaming":data}),200

@media_bp.route("/", methods=["GET"])
def lista_de_medios_por_pais():
    pais=request.args.get("pais")
    if not pais:
        return jsonify({'error':'Falta en la cadena de consulta ?pais=nombre_pais'}), 404
    data=[]
    for id_medio, medio in medios.items():
        if str(medio.get("pais", "")).lower() == str(pais).lower():
            data.append({"id_medio_de_streaming": id_medio, "medio": medio})
    if not data:
        return jsonify({'error':'No hay medios de streaming en ese pais'}), 404
    return jsonify({"medio_de_streaming": data}), 200

@media_bp.route("/", methods=["GET"])
def lista_de_medios_por_fecha():
    fecha_de_subida=request.args.get("fecha_subida")
    if not fecha_de_subida:
        return jsonify({'error':'Falta en la cadena de consulta ?fecha_subida=fecha'})
    data=[]
    for id_medio, medio in medios.items():
        if str(medio.get("fecha_subida", "")).lower()==str(fecha_subida).lower():
            data.append({"id_medio_de_streaming": id_medio, "medio": medio})
    if not data:
        return jsonify({'error':'No hay medios de streaming con esa fecha de subida'}), 404
    return jsonify({'medio_de_streaming':data}), 200

@media_bp.route("/<string:id_medio_de_streaming>", methods=["POST"])
def anadir_medio(id_medio_de_streaming):
    data=request.get_json()
    if not data:
        return jsonify({"Error": "JSON vacío"}), 400
    try:
        schema=MediaSchema()
        schema.load(data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 409
    
    medios[id_medio_de_streaming]={"pais": data["pais"], "fecha_de_subida": str(data["fecha_de_subida"])}
    return jsonify({"Mensaje": "Medio de streaming añadido"}), 201

@media_bp.route("/<string:id_medio_de_streaming>", methods=["DELETE"])
def eliminar_medio(id_medio_de_streaming):
    id_medio=medios.get(id_medio_de_streaming)
    if id_medio is not None:
        del medios[id_medio_de_streaming]
        return jsonify({"Mensaje": "Medio de streaming eliminado"}), 200
    else:
        return jsonify({"Error": "Medio no encontrado"}), 404
    
@media_bp.route("/", methods=["GET"])
def obtener_medios():
    return jsonify(medios), 200

@media_bp.route("/<string:id_medio_de_streaming>", methods=["DELETE"])
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

media_bp.route("/", methods=["GET"])
def medios_por_fecha_limite():
    fecha_de_subida=request.args.get("fecha_de_subida")
    num_items=request.args.get("num_items")
    if not fecha_de_subida or not num_items:
        return jsonify({"error":"Falta en la cadena de consulta ?fecha_subida=fecha"}), 404
    try:
        num_items=int(num_items)
    except:
        return jsonify({"Error": "num_items debe ser entero"}), 409
    
    data=[]
    for id_medio, medio in medios.items():
        if str(medio.get("fecha_de_subida", "")).lower==str(fecha_de_subida).lower():
            data.append({"id_medio_de_Streaming": id_medio, "medio":medio})
    if not dara:
        return jsonify({"Error":"No hay medios de streaming con esa fecha de subida"}), 404
    data=data[:num_items]
    return jsonify({"medio_de_streaming":data}), 200