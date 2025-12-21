from flask import Flask, jsonify, request, Blueprint
from marshmallow import Schema, fields, validate, ValidationError

from users_db import usuarios
from suscripciones_db import suscripciones

suscripciones_bp = Blueprint("suscripcion", __name__)


class SuscripcionSchema(Schema):
    id_suscripcion=fields.Int(required=True)
    tipo=fields.Str(required=True)
    precio=fields.Str(required=True)

@suscripciones_bp.route("/usuarios/<id_usuario>/suscripciones", methods=["POST"])
def pagar_suscripcion(id_usuario):
    id_usuario=int(id_usuario)
    data=request.get_json()
    if not data:
        return jsonify({'error':'Missing nssssss'}), 400
    try:
        schema=SuscripcionSchema()
        schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages),400
    if id_usuario not in [u["id_usuario"] for u in usuarios.values()]:
        return jsonify({'error':'No existe usuario'}), 404
    suscripciones[str(id_usuario)]=data
    return jsonify({"suscripcion":data}),200

@suscripciones_bp.route("/usuarios/<id_usuario>/suscripciones", methods=["DELETE"])
def cancelar_suscripcion(id_usuario):
    id_usuario = int(id_usuario)
    if id_usuario not in [u["id_usuario"] for u in usuarios.values()]:
        return jsonify({'error':'No existe usuario'}), 404
    if str(id_usuario) not in suscripciones:
        return jsonify({'error':'No existe suscripcion'}),404
    del suscripciones[str(id_usuario)]
    return jsonify({'mensaje':'suscripcion cancelada'}),200