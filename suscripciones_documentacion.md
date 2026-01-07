# Documentación de Endpoints - Suscripciones

Esta documentación describe los endpoints disponibles en el módulo de suscripciones (`suscripciones_bp.py`) de la API de Streaming.

**Base URL:** `/usuarios`

---

## Estructura de Datos

### `suscripciones`

Las suscripciones de usuarios se almacenan en memoria como un diccionario Python donde la clave es el ID del usuario y el valor es un objeto con los datos de la suscripción.

```python
suscripciones = {
    "id_usuario": {
        "id_suscripcion": 1,
        "tipo": "Premium",
        "precio": "9.99"
    }
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_usuario` (clave) | `string` | ID del usuario (debe existir en `users_db`) |
| `id_suscripcion` | `integer` | Identificador único de la suscripción |
| `tipo` | `string` | Tipo de suscripción (ej. Básica, Premium, Pro) |
| `precio` | `string` | Precio de la suscripción |

> [!IMPORTANT]
> Los datos se almacenan en memoria (`suscripciones_db.py`), por lo que se pierden al reiniciar el servidor.

---

## Endpoints

### 1. Consultar Suscripción Activa

**Endpoint:** `GET /usuarios/<id_usuario>/suscripciones`

🔐 **Requiere Token JWT**

Obtiene la suscripción activa de un usuario específico. Solo el propio usuario puede consultar su suscripción.

#### Request

**Headers:**
```
Authorization: Bearer <token_jwt>
```

**Parámetros de URL:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id_usuario` | `string` | ID del usuario cuya suscripción se quiere consultar |

No requiere body.

#### Responses

**✅ Éxito (200):**
```json
{
    "mensaje": {
        "id_suscripcion": 1,
        "tipo": "Premium",
        "precio": "9.99"
    }
}
```

**❌ No autorizado (403):**
```json
{
    "error": "No autorizado"
}
```
*Ocurre si intentas consultar la suscripción de otro usuario.*

**❌ Suscripción no encontrada (404):**
```json
{
    "Error": "Suscripción no encontrada o usuario no tiene suscripción activa"
}
```

---

### 2. Pagar/Activar Suscripción

**Endpoint:** `POST /usuarios/<id_usuario>/suscripciones`

🔐 **Requiere Token JWT**

Registra o activa una suscripción para un usuario específico. Solo el propio usuario puede pagar su suscripción.

#### Request

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <token_jwt>
```

**Parámetros de URL:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id_usuario` | `string` | ID del usuario que va a pagar la suscripción |

**Body (JSON):**
```json
{
    "id_suscripcion": 1,
    "tipo": "Premium",
    "precio": "9.99"
}
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id_suscripcion` | `integer` | ✅ Sí | ID de la suscripción |
| `tipo` | `string` | ✅ Sí | Tipo de suscripción |
| `precio` | `string` | ✅ Sí | Precio de la suscripción |

#### Responses

**✅ Suscripción activada (200):**
```json
{
    "suscripcion": {
        "id_suscripcion": 1,
        "tipo": "Premium",
        "precio": "9.99"
    }
}
```

**❌ No autorizado (403):**
```json
{
    "error": "No autorizado"
}
```
*Ocurre si intentas pagar la suscripción de otro usuario.*

**❌ Usuario no encontrado (404):**
```json
{
    "error": "No existe usuario"
}
```
*Ocurre si el `id_usuario` no existe en `users_db`.*

**❌ Falta JSON (400):**
```json
{
    "error": "Missing JSON"
}
```
*Ocurre si no se envía body.*

**❌ Error de validación (400):**
```json
{
    "campo": ["mensaje de error"]
}
```
*Ocurre si los datos no cumplen con el esquema (ej. tipo incorrecto o campo faltante).*

---

### 3. Modificar Suscripción

**Endpoint:** `PUT /usuarios/<id_usuario>/suscripciones`

🔐 **Requiere Token JWT**

Modifica los datos de una suscripción existente. Solo el propio usuario puede modificar su suscripción.

#### Request

**Headers:**
```
Content-Type: application/json
```

**Parámetros de URL:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id_usuario` | `string` | ID del usuario |

**Body (JSON):**
```json
{
    "id_suscripcion": 2,
    "tipo": "Premium Plus",
    "precio": "14.99"
}
```

#### Responses

**✅ Éxito (200):**
```json
{
    "suscripcion": {
        "id_suscripcion": 2,
        "tipo": "Premium Plus",
        "precio": "14.99"
    }
}
```

**❌ No autorizado (403):**
```json
{
    "error": "No autorizado"
}
```
*Ocurre si intentas modificar la suscripción de otro usuario.*

**❌ No encontrado (404):**
- Usuario no existe: `{"error": "No existe usuario"}`
- Suscripción no existe: `{"error": "No existe suscripcion"}`

---

### 4. Cancelar Suscripción

**Endpoint:** `DELETE /usuarios/<id_usuario>/suscripciones`

🔐 **Requiere Token JWT**

Cancela la suscripción activa de un usuario. Solo el propio usuario puede cancelar su suscripción.

#### Request

**Parámetros de URL:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id_usuario` | `string` | ID del usuario cuya suscripción se va a cancelar |

No requiere body.

#### Responses

**✅ Suscripción cancelada (200):**
```json
{
    "mensaje": "suscripcion cancelada"
}
```

**❌ No autorizado (403):**
```json
{
    "error": "No autorizado"
}
```
*Ocurre si intentas cancelar la suscripción de otro usuario.*

**❌ Usuario no encontrado (404):**
```json
{
    "error": "No existe usuario"
}
```
*Ocurre si el `id_usuario` no existe en `users_db`.*

**❌ Suscripción no encontrada (404):**
```json
{
    "error": "No existe suscripcion"
}
```
*Ocurre si el usuario no tiene una suscripción activa.*

---

## Esquemas de Validación

El módulo utiliza **Marshmallow** para validar los datos de entrada:

### SuscripcionSchema
```python
class SuscripcionSchema(Schema):
    id_suscripcion = fields.Int(required=True)
    tipo = fields.Str(required=True)
    precio = fields.Str(required=True)
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id_suscripcion` | `integer` | ✅ Sí | ID de la suscripción |
| `tipo` | `string` | ✅ Sí | Tipo de suscripción |
| `precio` | `string` | ✅ Sí | Precio de la suscripción |

---

## Dependencias

| Librería | Uso |
|----------|-----|
| `Flask` | Framework web |
| `flask_jwt_extended` | Autenticación con tokens JWT |
| `marshmallow` | Validación de esquemas |
| `users_bp` | Verificación de existencia de usuarios (`users_db`) |
| `suscripciones_db` | Almacenamiento de suscripciones |

---

## Notas Adicionales

> [!NOTE]
> Cada usuario solo puede tener una suscripción activa a la vez. Al registrar una nueva suscripción, se sobrescribe la anterior.

> [!TIP]
> Antes de pagar una suscripción, asegúrate de que el usuario esté registrado en el sistema usando los endpoints de `/usuarios/register`.

Prompt Utilizado

Crea una documentacion para @suscripciones_bp.py basandote en las otras documentaciones, es decir, @media_documentacion.md, @users_documentacion.md y @historial_documentacion.md
 