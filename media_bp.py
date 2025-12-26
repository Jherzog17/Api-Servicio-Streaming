from flask import Flask, jsonify, request, Blueprint
from marshmallow import Schema, fields, validate, ValidationError

from media_db import medios

media_bp = Blueprint("medio_de_streaming", __name__)

class MediaSchema(Schema):
    id_medio_de_streaming=fields.Int(required=True)
    pais=fields.Str(required=True)
    fecha_de_subida=fields.Date(required=True)

@media_bp.route("/<string:id_medio_de_streaming>", methods=["GET"])
def reproducir_medio_de_streaming(id_medio_de_streaming):
    data=media_bp.get(id_medio_de_streaming)
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
    fecha_subida=request.args.get("fecha_subida")
    if not fecha_subida:
        return jsonify({'error':'Falta en la cadena de consulta ?fecha_subida=fecha'})
    data=[]
    for id_medio, medio in medios.items():
        if str(medio.get("fecha_subida", "")).lower()==str(fecha_subida).lower():
            data.append({"id_medio_de_streaming": id_medio, "medio": medio})
    if not data:
        return jsonify({'error':'No hay medios de streaming con esa fecha de subida'}), 404
    return jsonify({'medio_de_streaming':data}), 200