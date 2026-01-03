# Documentación de Endpoints - Usuarios

Esta documentación describe los endpoints disponibles en el módulo de usuarios (`users_bp.py`) de la API de Streaming.

**Base URL:** `/usuarios`

---

## Estructura de Datos

### `users_db`

La base de datos de usuarios se almacena en memoria como un diccionario Python con la siguiente estructura:

```python
users_db = {
    "id_usuario": {
        "nickname": "nombre_usuario",
        "password": "contraseña_hasheada"
    }
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_usuario` (clave) | `string` | UUID único generado automáticamente con `uuid.uuid4().hex` |
| `nickname` | `string` | Nombre de usuario |
| `password` | `string` | Contraseña encriptada usando `werkzeug.security.generate_password_hash` |

> [!IMPORTANT]
> Los datos se almacenan en memoria, por lo que se pierden al reiniciar el servidor.

---

## Endpoints

### 1. Registro de Usuario

**Endpoint:** `POST /usuarios/register`

Registra un nuevo usuario en el sistema.

#### Request

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "nickname": "nombre_de_usuario",
    "password": "contraseña_del_usuario"
}
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `nickname` | `string` | ✅ Sí | Nombre de usuario para el registro |
| `password` | `string` | ✅ Sí | Contraseña del usuario |

#### Responses

**✅ Registro exitoso (200):**
```json
{
    "Mensaje": "Usuario registrado correctamente"
}
```

**❌ JSON vacío (400):**
```json
{
    "Error": "JSON vacío, debe introducir un JSON con usuario y contraseña"
}
```

**❌ Error de validación (409):**
```json
{
    "Error": {
        "campo": ["mensaje de error"]
    }
}
```

---

### 2. Inicio de Sesión (Login)

**Endpoint:** `POST /usuarios/login`

Autentica a un usuario y devuelve un token JWT.

#### Request

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "nickname": "nombre_de_usuario",
    "password": "contraseña_del_usuario"
}
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `nickname` | `string` | ✅ Sí | Nombre de usuario registrado |
| `password` | `string` | ✅ Sí | Contraseña del usuario |

#### Responses

**✅ Login exitoso (200):**
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

> [!NOTE]
> El token JWT se genera usando el `id` del usuario como identidad.

**❌ Error de validación (409):**
```json
{
    "Error": {
        "campo": ["mensaje de error"]
    }
}
```

**❌ Contraseña incorrecta (409):**
```json
{
    "Error": "Contraseña incorrecta"
}
```

**❌ Usuario no encontrado (404):**
```json
{
    "Error": "Usuario no encontrado"
}
```

---

### 3. Obtener Usuarios

**Endpoint:** `GET /usuarios/`

Devuelve todos los usuarios registrados en el sistema.

#### Request

No requiere body ni parámetros.

#### Response

**✅ Éxito (200):**
```json
{
    "abc123def456...": {
        "nickname": "usuario1",
        "password": "$pbkdf2-sha256$..."
    },
    "ghi789jkl012...": {
        "nickname": "usuario2",
        "password": "$pbkdf2-sha256$..."
    }
}
```

> [!WARNING]
> Este endpoint devuelve las contraseñas hasheadas. En un entorno de producción, se recomienda proteger este endpoint o filtrar los datos sensibles.

---

### 4. Editar Usuario

**Endpoint:** `PUT /usuarios/<id_usuario>`

🔐 **Requiere Token JWT**

Edita los datos de un usuario existente. Solo el propio usuario puede editar su cuenta.

#### Request

**Headers:**
```
Content-Type: application/json
```

**Parámetros de URL:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id_usuario` | `string` | UUID del usuario a editar |

**Body (JSON):**
```json
{
    "nickname": "nuevo_nombre",
    "password": "nueva_contraseña"
}
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `nickname` | `string` | ❌ No | Nuevo nombre de usuario |
| `password` | `string` | ❌ No | Nueva contraseña (se hasheará automáticamente) |

> [!NOTE]
> Puedes enviar uno o ambos campos. Solo se actualizarán los campos enviados.

#### Responses

**✅ Edición exitosa (200):**
```json
{
    "mensaje": "Usuario editado con éxito"
}
```

**❌ ID no válido (404):**
```json
{
    "Error": "ID introducido no válido"
}
```

**❌ Sin campos para cambiar (409):**
```json
{
    "Error": "No hay campos para cambiar"
}
```

---

### 5. Eliminar Usuario

**Endpoint:** `DELETE /usuarios/<id_usuario>`

🔐 **Requiere Token JWT**

Elimina un usuario del sistema. Solo el propio usuario puede eliminarse.

#### Request

**Parámetros de URL:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id_usuario` | `string` | UUID del usuario a eliminar |

No requiere body.

#### Responses

**✅ Eliminación exitosa (200):**
```json
{
    "mensaje": "Usuario eliminado con éxito"
}
```

**❌ Usuario no encontrado (404):**
```json
{
    "Error": "Usuario no encontrado"
}
```

---

## Esquemas de Validación

El módulo utiliza **Marshmallow** para validar los datos de entrada:

### UsersSchema (para registro y login)
```python
class UsersSchema(Schema):
    nickname = fields.Str(required=True)
    password = fields.Str(required=True)
```

### EditUsersSchema (para edición)
```python
class EditUsersSchema(Schema):
    nickname = fields.Str(required=False)
    password = fields.Str(required=False)
```

---

## Dependencias

| Librería | Uso |
|----------|-----|
| `Flask` | Framework web |
| `flask_jwt_extended` | Generación de tokens JWT |
| `uuid` | Generación de IDs únicos |
| `werkzeug.security` | Hash y verificación de contraseñas |
| `marshmallow` | Validación de esquemas |


# Prompt Utilizado 
basandote en @users_bp.py quiero que crees un archivo que sea users_documentacion.md donde aparezcan todos los endpoints de esta seccion, como se usan, los campos requeridos  en el body al hacer el post y tambien detallar como se guardan los datos, es decir, users_db


