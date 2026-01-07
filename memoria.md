# Memoria - API de Servicio de Streaming

**Asignatura:** Representación e intercambio de datos
**Curso:** 2025-2026  
**Fecha:** 7 de enero de 2026

---

## Integrantes del Grupo

| Nombre | Rol |
|--------|-----|
| *[Nombre del integrante 1]* | Desarrollo y documentación |
| *[Nombre del integrante 2]* | Desarrollo y testing |
| *[Nombre del integrante 3]* | Desarrollo y revisión |
| *[Nombre del integrante 4]* | Desarrollo y coordinación |

> **Nota:** Completar con los nombres reales de los integrantes del grupo.

---

## a) Scripts Desarrollados

El proyecto está compuesto por los siguientes scripts:

### 1. `backend.py` - Servidor Principal

**Descripción:** Archivo principal de la aplicación Flask que inicializa el servidor y registra todos los blueprints.

**Contenido:**
- Configuración de Flask y JWT
- Registro de blueprints con sus prefijos de URL:
  - `/usuarios` → `users_bp`
  - `/medio_de_streaming` → `media_bp`
  - `historial_bp` (sin prefijo, rutas completas definidas en el blueprint)
  - `suscripciones_bp` (sin prefijo, rutas completas definidas en el blueprint)

```python
from flask import Flask
from flask_jwt_extended import JWTManager
from users_bp import users_bp
from media_bp import media_bp
from historial_bp import historial_bp
from suscripciones_bp import suscripciones_bp
import os

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

app.register_blueprint(users_bp, url_prefix="/usuarios")
app.register_blueprint(media_bp, url_prefix="/medio_de_streaming")
app.register_blueprint(historial_bp)
app.register_blueprint(suscripciones_bp)
```

---

### 2. `users_bp.py` - Blueprint de Usuarios

**Descripción:** Gestiona todas las operaciones relacionadas con usuarios: registro, login, edición y eliminación.

**Características principales:**
- **Autenticación JWT:** Generación de tokens para login
- **Hash de contraseñas:** Uso de `werkzeug.security` para almacenar contraseñas de forma segura
- **Validación con Marshmallow:** Schemas `UsersSchema` y `EditUsersSchema`
- **Generación de IDs únicos:** Uso de `uuid.uuid4().hex`

**Endpoints:**
- `POST /usuarios/register` - Registro de usuarios
- `POST /usuarios/login` - Inicio de sesión (devuelve JWT)
- `GET /usuarios/` - Listar usuarios
- `PUT /usuarios/<id>` - Editar usuario (🔐 JWT)
- `DELETE /usuarios/<id>` - Eliminar usuario (🔐 JWT)

---

### 3. `media_bp.py` - Blueprint de Medios

**Descripción:** Gestiona la colección de medios de streaming (películas, series, etc.).

**Características principales:**
- **Filtrado por query params:** país, fecha de subida, límite de items
- **Protección JWT:** Para reproducir medios
- **Validación con Marshmallow:** Schema `MediaSchema`

**Endpoints:**
- `GET /medio_de_streaming/` - Listar medios (con filtros opcionales)
- `GET /medio_de_streaming/<id>` - Reproducir medio (🔐 JWT)
- `POST /medio_de_streaming/anadir_medio` - Añadir medio
- `PUT /medio_de_streaming/<id>` - Editar medio
- `DELETE /medio_de_streaming/<id>` - Eliminar medio

---

### 4. `historial_bp.py` - Blueprint de Historial

**Descripción:** Gestiona el historial de visualización de cada usuario.

**Características principales:**
- **Protección JWT:** Solo el propio usuario puede ver/modificar su historial
- **Verificación de existencia:** Comprueba que el medio existe antes de añadirlo
- **Validación con Marshmallow:** Schema `HistorialItemSchema`

**Endpoints:**
- `GET /usuarios/<id>/historial` - Consultar historial (🔐 JWT)
- `POST /usuarios/<id>/historial` - Añadir al historial (🔐 JWT)

---

### 5. `suscripciones_bp.py` - Blueprint de Suscripciones

**Descripción:** Gestiona las suscripciones de los usuarios.

**Características principales:**
- **Protección JWT:** Todas las operaciones requieren autenticación
- **Un usuario = Una suscripción:** Se sobrescribe al crear una nueva
- **Validación con Marshmallow:** Schema `SuscripcionSchema`

**Endpoints:**
- `GET /usuarios/<id>/suscripciones` - Consultar suscripción (🔐 JWT)
- `POST /usuarios/<id>/suscripciones` - Pagar/Activar suscripción (🔐 JWT)
- `PUT /usuarios/<id>/suscripciones` - Modificar suscripción (🔐 JWT)
- `DELETE /usuarios/<id>/suscripciones` - Cancelar suscripción (🔐 JWT)

---

### 6. Bases de Datos en Memoria

| Archivo | Variable | Descripción |
|---------|----------|-------------|
| `users_bp.py` | `users_db` | Diccionario de usuarios |
| `media_db.py` | `medios` | Diccionario de medios |
| `historial_db.py` | `historial` | Diccionario de historiales |
| `suscripciones_db.py` | `suscripciones` | Diccionario de suscripciones |

---

### 7. `test_api.py` - Cliente de Pruebas

**Descripción:** Script interactivo para probar todos los endpoints de la API.

**Características:**
- Menú interactivo con opciones numeradas
- Gestión automática de tokens JWT
- Pruebas individuales para cada endpoint
- Formateo de respuestas JSON

---

## b) Árbol de Endpoints

```
API de Streaming (http://127.0.0.1:5000)
│
├── /usuarios
│   ├── POST   /register          → Registrar usuario
│   ├── POST   /login             → Iniciar sesión (devuelve JWT)
│   ├── GET    /                  → Listar usuarios
│   ├── PUT    /<id_usuario>      → Editar usuario [🔐 JWT]
│   ├── DELETE /<id_usuario>      → Eliminar usuario [🔐 JWT]
│   │
│   ├── /<id_usuario>/historial
│   │   ├── GET                   → Consultar historial [🔐 JWT]
│   │   └── POST                  → Añadir al historial [🔐 JWT]
│   │
│   └── /<id_usuario>/suscripciones
│       ├── GET                   → Consultar suscripción [🔐 JWT]
│       ├── POST                  → Pagar suscripción [🔐 JWT]
│       ├── PUT                   → Modificar suscripción [🔐 JWT]
│       └── DELETE                → Cancelar suscripción [🔐 JWT]
│
└── /medio_de_streaming
    ├── GET    /                  → Listar medios
    │          ?pais=...          → Filtrar por país
    │          ?fecha_subida=...  → Filtrar por fecha
    │          ?num_items=...     → Limitar resultados
    ├── GET    /<id>              → Reproducir medio [🔐 JWT]
    ├── POST   /anadir_medio      → Añadir medio
    ├── PUT    /<id>              → Editar medio
    └── DELETE /<id>              → Eliminar medio
```

---

## c) Operaciones Implementadas

### c.1) Usuarios

#### Registrar Usuario

**Endpoint:** `POST /usuarios/register`

**Código implementado:**
```python
@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"Error": "JSON vacío, debe introducir un JSON con usuario y contraseña"}), 400
    
    try:
        schema = UsersSchema()
        schema.load(data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 409
    
    id_usuario = uuid.uuid4().hex
    contrasena_codificada = generate_password_hash(data["password"])
    users_db[id_usuario] = {"nickname": data["nickname"], "password": contrasena_codificada}
    
    return jsonify({"Mensaje": "Usuario registrado correctamente"}), 200
```

**Decisiones de diseño:**
- Se genera un UUID aleatorio para garantizar unicidad
- La contraseña se hashea con `werkzeug.security` para seguridad
- Se valida el schema con Marshmallow antes de procesar

**Test con terminal:**
```bash
curl -X POST http://127.0.0.1:5000/usuarios/register \
  -H "Content-Type: application/json" \
  -d '{"nickname": "test_user", "password": "test123"}'

# Respuesta esperada:
# {"Mensaje": "Usuario registrado correctamente"}
```

---

#### Login de Usuario

**Endpoint:** `POST /usuarios/login`

**Código implementado:**
```python
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
                access_token = create_access_token(identity=id)
                return jsonify({"token": access_token}), 200
            else:
                return jsonify({"Error": "Contraseña incorrecta"}), 409
    return jsonify({'Error': 'Usuario no encontrado'}), 404
```

**Decisiones de diseño:**
- El token JWT se genera usando el `id_usuario` como identidad
- Se verifica la contraseña hasheada con `check_password_hash`

---

#### Editar Usuario

**Endpoint:** `PUT /usuarios/<id_usuario>` 🔐

**Código implementado:**
```python
@users_bp.route("/<string:id_usuario>", methods=["PUT"])
@jwt_required()
def editar_usuario(id_usuario):
    current_user = get_jwt_identity()
    if current_user != id_usuario:
        return jsonify({"Error": "No autorizado para editar este usuario"}), 403
    
    data = request.get_json()
    # ... validación y actualización
    for campo, valor in data.items():
        if campo == "password":
            new_value = generate_password_hash(valor)
        else:
            new_value = valor
        users_db[id_usuario][campo] = new_value
    return jsonify({"mensaje": "Usuario editado con éxito"}), 200
```

**Decisiones de diseño:**
- Solo el propio usuario puede editar su cuenta (verificación JWT)
- Si se cambia la contraseña, se hashea automáticamente

---

#### Eliminar Usuario

**Endpoint:** `DELETE /usuarios/<id_usuario>` 🔐

**Código implementado:**
```python
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
```

---

### c.2) Medios de Streaming

#### Listar Medios (con Filtros)

**Endpoint:** `GET /medio_de_streaming/?pais=...&fecha_subida=...&num_items=...`

**Código implementado:**
```python
@media_bp.route("/", methods=["GET"])
def listar_medios():
    pais = request.args.get("pais")
    fecha_subida = request.args.get("fecha_subida")
    num_items = request.args.get("num_items")
    
    # Filtrar por país
    if pais:
        data = []
        for id_medio, medio in medios.items():
            if str(medio.get("pais", "")).lower() == str(pais).lower():
                data.append({"id_medio_de_streaming": id_medio, "medio": medio})
        # ...
    
    # Filtrar por fecha (con límite opcional)
    if fecha_subida:
        # ...
        if num_items:
            data = data[:int(num_items)]
    
    return jsonify(medios), 200
```

**Decisiones de diseño:**
- Comparación case-insensitive para países
- El parámetro `num_items` solo aplica junto con `fecha_subida`

---

#### Reproducir Medio

**Endpoint:** `GET /medio_de_streaming/<id>` 🔐

**Código implementado:**
```python
@media_bp.route("/<int:id_medio_de_streaming>", methods=["GET"])
@jwt_required()
def reproducir_medio_de_streaming(id_medio_de_streaming):
    data = medios.get(id_medio_de_streaming)
    if not data:
        return jsonify({'error': 'Medio not found'}), 404
    return jsonify({"medio_de_streaming": data}), 200
```

**Decisiones de diseño:**
- Requiere autenticación JWT para simular que solo usuarios registrados pueden ver contenido

---

#### Añadir Medio

**Endpoint:** `POST /medio_de_streaming/anadir_medio`

**Código implementado:**
```python
@media_bp.route("/anadir_medio", methods=["POST"])
def anadir_medio():
    data = request.get_json()
    if not data:
        return jsonify({"Error": "JSON vacío"}), 400
    try:
        schema = MediaSchema()
        schema.load(data)
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 409
    
    medios[data["id_medio_de_streaming"]] = {
        "pais": data["pais"], 
        "fecha_de_subida": str(data["fecha_de_subida"])
    }
    return jsonify({"Mensaje": "Medio de streaming añadido"}), 201
```

---

### c.3) Historial

#### Consultar Historial

**Endpoint:** `GET /usuarios/<id>/historial` 🔐

**Código implementado:**
```python
@historial_bp.route("/usuarios/<id_usuario>/historial", methods=["GET"])
@jwt_required()
def consultar_historial(id_usuario):
    current_user = get_jwt_identity()
    if current_user != id_usuario:
        return jsonify({"error": "No autorizado para ver este historial"}), 403
    
    if id_usuario not in users_db:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    lista_historial = historial.get(id_usuario, [])
    return jsonify({"historial": lista_historial}), 200
```

---

#### Añadir al Historial

**Endpoint:** `POST /usuarios/<id>/historial` 🔐

**Código implementado:**
```python
@historial_bp.route("/usuarios/<id_usuario>/historial", methods=["POST"])
@jwt_required()
def anadir_al_historial(id_usuario):
    current_user = get_jwt_identity()
    if current_user != id_usuario:
        return jsonify({"error": "No autorizado para modificar este historial"}), 403
    
    data = request.get_json()
    # Verificar que el medio existe
    if data['id_medio_de_streaming'] not in medios:
        return jsonify({'error': 'El medio de streaming no existe'}), 404
    
    if id_usuario not in historial:
        historial[id_usuario] = []
    historial[id_usuario].append(data)
    
    return jsonify({"mensaje": "Añadido al historial", "historial": historial[id_usuario]}), 201
```

**Decisiones de diseño:**
- Se verifica que el medio existe antes de añadirlo al historial
- Si el usuario no tiene historial, se crea una lista vacía

---

### c.4) Suscripciones

#### Pagar Suscripción

**Endpoint:** `POST /usuarios/<id>/suscripciones` 🔐

```python
@suscripciones_bp.route("/usuarios/<id_usuario>/suscripciones", methods=["POST"])
@jwt_required()
def pagar_suscripcion(id_usuario):
    current_user = get_jwt_identity()
    if current_user != id_usuario:
        return jsonify({"error": "No autorizado"}), 403
    
    data = request.get_json()
    # Validación...
    suscripciones[id_usuario] = data
    return jsonify({"suscripcion": data}), 200
```

---

#### Cancelar Suscripción

**Endpoint:** `DELETE /usuarios/<id>/suscripciones` 🔐

```python
@suscripciones_bp.route("/usuarios/<id_usuario>/suscripciones", methods=["DELETE"])
@jwt_required()
def cancelar_suscripcion(id_usuario):
    current_user = get_jwt_identity()
    if current_user != id_usuario:
        return jsonify({"error": "No autorizado"}), 403
    
    if id_usuario not in suscripciones:
        return jsonify({'error': 'No existe suscripcion'}), 404
    
    del suscripciones[id_usuario]
    return jsonify({'mensaje': 'suscripcion cancelada'}), 200
```

---

## d) Problemas Encontrados y Soluciones

### Problemas Corregidos ✅

| # | Problema | Solución |
|---|----------|----------|
| 1 | **Rutas duplicadas en `media_bp.py`** - Había 3 funciones con la misma ruta GET `/` | Se combinaron en una sola función `listar_medios()` que maneja todos los query params |
| 2 | **Método HTTP incorrecto** - `editar_medio` usaba DELETE en vez de PUT | Se cambió a PUT |
| 3 | **Función huérfana** - `medios_por_fecha_limite()` sin decorador de ruta | Se integró en `listar_medios()` |
| 4 | **Typo `.lower` sin paréntesis** | Se corrigió a `.lower()` |
| 5 | **Uso incorrecto de `media_bp.get()`** | Se cambió a `medios.get(id)` |
| 6 | **Rutas inconsistentes en `backend.py`** | Se quitaron prefijos incorrectos de `historial_bp` y `suscripciones_bp` |
| 7 | **URLs incorrectas en `test_api.py`** | Se actualizaron todas las URLs |
| 8 | **Typo en clave de error** | Se corrigió `"Error:"` a `"Error"` |

### Advertencias Pendientes ⚠️

| # | Advertencia | Estado |
|---|-------------|--------|
| 1 | **Datos en memoria** - Se pierden al reiniciar | Intencional para simplificar el desarrollo |
| 2 | **JWT_SECRET_KEY puede ser None** | Añadir valor por defecto o documentar configuración |
| 3 | **Contraseñas hasheadas expuestas** en GET /usuarios/ | Considerar filtrar este campo en producción |

### Inconsistencias Menores

- El query param usa `fecha_subida` pero el schema define `fecha_de_subida` (intencional para simplificar URLs)

---

## e) Modificaciones Respecto a la P3

### Cambios Implementados

| Diseño Original (P3) | Implementación Final | Justificación |
|---------------------|---------------------|---------------|
| URI: `/suscripcion/<id_suscripcion>` | URI: `/usuarios/<id>/suscripciones` | Más RESTful, la suscripción es un subrecurso del usuario |
| URI: `/usuario/<id>/historial` (singular) | URI: `/usuarios/<id>/historial` (plural) | Consistencia con el resto de endpoints |
| ID de usuario numérico | ID de usuario UUID | Mayor seguridad y evita colisiones |
| Campo `suscripcion` en Usuario | Suscripción como recurso separado | Mejor separación de responsabilidades |
| POST en `/medio_de_streaming/<id>` | POST en `/medio_de_streaming/anadir_medio` | Evitar confusión con GET de un medio específico |

### Funcionalidades Adicionales

1. **Autenticación JWT** - No especificada en P3, pero necesaria para seguridad
2. **Validación con Marshmallow** - Schemas para validar datos de entrada
3. **Hash de contraseñas** - Seguridad adicional
4. **Script de pruebas interactivo** - `test_api.py` para facilitar testing

### Funcionalidades No Implementadas

| Funcionalidad de P3 | Motivo |
|---------------------|--------|
| Filtrado por rango de fechas (`fecha_min`, `fecha_max`) | Simplificación, se implementó solo `fecha_subida` exacta |
| Paginación en `/usuarios` | No era prioritario para el MVP |

---

## Anexo: Ejecutar la API

### Requisitos
```bash
pip install flask flask-jwt-extended marshmallow werkzeug
```

### Variables de Entorno
```bash
export JWT_SECRET_KEY="tu_clave_secreta"
```

### Iniciar Servidor
```bash
python backend.py
```

### Ejecutar Tests
```bash
python test_api.py
```

---

*Documento generado el 7 de enero de 2026*
