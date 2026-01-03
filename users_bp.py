from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, validate, ValidationError

users_db = {}

users_bp= Blueprint("usuarios", __name__)

class UsersSchema(Schema):
    nickname = fields.Str(required=True)
    password = fields.Str(required=True)

class EditUsersSchema(Schema):
    nickname = fields.Str(required=False)
    password = fields.Str(required=False)


@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()#Obtener el json del post que lleva el usuario y la contraseña

    if not data:
        return jsonify({"Error": "JSON vacío, debe introducir un JSON con usuario y contraseña"}), 400

    #Comprobar que tiene la estuctura correcta el post
    try:
        schema = UsersSchema()
        schema.load(data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 409

    
    id_usuario = uuid.uuid4().hex
    contrasena_codificada = generate_password_hash(data["password"])
    users_db[id_usuario]= {"nickname" : data["nickname"],"password" : contrasena_codificada}#Agregar al nuevo usuario

    return jsonify({"Mensaje": "Usuario registrado correctamente"}), 200

@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        schema = UsersSchema()
        schema.load(data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 409

    for id, valor in users_db.items():
        if users_db.get(id).get("nickname") == data["nickname"]:
            if check_password_hash(users_db[id]["password"], data["password"]): 
                access_token = create_access_token(identity=id)#Crea el token a partir del id del usuario
                return jsonify({"token": access_token}), 200
            else:
                return jsonify({"Error": "Contraseña incorrecta"}), 409
    return jsonify({'Error': 'Usuario no encontrado'}), 404
    
@users_bp.route("/", methods=["GET"])
def obtener_usuarios():
    return jsonify(users_db), 200


@users_bp.route("/<string:id_usuario>", methods=["PUT"])
@jwt_required()
def editar_usuario(id_usuario):
    current_user = get_jwt_identity()
    if current_user != id_usuario:
        return jsonify({"Error": "No autorizado para editar este usuario"}), 403
    
    data = request.get_json()
    try:
        schema = EditUsersSchema()
        schema.load(data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}),400
    usuario = users_db.get(id_usuario)
    if usuario is None:
        return jsonify({"Error": "ID introducido no válido"}),404
    if not data:
        return jsonify({"Error": "No hay campos para cambiar"}),409
    for campo, valor in data.items():
        if campo == "password":
            new_value= generate_password_hash(valor)
        else:
            new_value = valor
        users_db[id_usuario][campo] = new_value
    return jsonify({"mensaje": "Usuario editado con éxito"}), 200


@users_bp.route("/<string:id_usuario>", methods=["DELETE"])
@jwt_required()
def eliminar_usuario(id_usuario):
    current_user = get_jwt_identity()
    if current_user != id_usuario:
        return jsonify({"Error": "No autorizado para eliminar este usuario"}), 403
    
    existe_id = users_db.get(id_usuario)
    if existe_id is not None:
        del users_db[id_usuario]
        return jsonify({"mensaje": "Usuario eliminado con éxito"}), 200
    else:
        return jsonify({"Error": "Usuario no encontrado"}), 404