# Documentación de Endpoints - Historial de Usuarios

Esta documentación describe los endpoints disponibles en el módulo de historial (`historial_bp.py`) de la API de Streaming.

**Base URL:** `/usuarios`

---

## Estructura de Datos

### `historial`

El historial de visualización de los usuarios se almacena en memoria como un diccionario Python donde la clave es el ID del usuario y el valor es una lista de medios vistos.

```python
historial = {
    "id_usuario": [
        {
            "id_medio_de_streaming": 123,
            "fecha_visualizacion": "YYYY-MM-DD"
        }
    ]
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_usuario` (clave) | `string` | ID del usuario (debe existir en `users_db`) |
| `id_medio_de_streaming` | `integer` | Identificador del medio visualizado |
| `fecha_visualizacion` | `date` | Fecha de visualización (opcional) |

> [!IMPORTANT]
> Los datos se almacenan en memoria (`historial_db.py`), por lo que se pierden al reiniciar el servidor.

---

## Endpoints

### 1. Consultar Historial

**Endpoint:** `GET /usuarios/<id_usuario>/historial`

🔐 **Requiere Token JWT**

Devuelve el historial de visualización de un usuario específico. Solo el propio usuario puede ver su historial.

#### Request

**Parámetros de URL:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id_usuario` | `string` | ID del usuario cuyo historial se quiere consultar |

No requiere body.

#### Responses

**✅ Éxito (200):**
```json
{
    "historial": [
        {
            "id_medio_de_streaming": 123,
            "fecha_visualizacion": "2024-01-01"
        }
    ]
}
```

**❌ Usuario no encontrado (404):**
```json
{
    "error": "Usuario no encontrado"
}
```
*Ocurre si el `id_usuario` no existe en `users_db`.*

---

### 2. Añadir al Historial

**Endpoint:** `POST /usuarios/<id_usuario>/historial`

🔐 **Requiere Token JWT**

Añade un nuevo registro de visualización al historial de un usuario. Solo el propio usuario puede añadir a su historial.

#### Request

**Headers:**
```
Content-Type: application/json
```

**Parámetros de URL:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id_usuario` | `string` | ID del usuario al que se añadirá el historial |

**Body (JSON):**
```json
{
    "id_medio_de_streaming": 123,
    "fecha_visualizacion": "2024-01-01"
}
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id_medio_de_streaming` | `integer` | ✅ Sí | ID del medio visualizado |
| `fecha_visualizacion` | `date` | ❌ No | Fecha de la visualización (formato YYYY-MM-DD) |

#### Responses

**✅ Añadido correctamente (201):**
```json
{
    "mensaje": "Añadido al historial",
    "historial": [
        {
            "id_medio_de_streaming": 123,
            "fecha_visualizacion": "2024-01-01"
        }
    ]
}
```

**❌ Usuario no encontrado (404):**
```json
{
    "error": "Usuario no encontrado"
}
```

**❌ Falta JSON o JSON inválido (400):**
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
*Ocurre si los datos no cumplen con el esquema (ej. tipo incorrecto).*

---

## Esquemas de Validación

El módulo utiliza **Marshmallow** para validar los datos de entrada:

### HistorialItemSchema
```python
class HistorialItemSchema(Schema):
    id_medio_de_streaming = fields.Int(required=True)
    fecha_visualizacion = fields.Date(required=False)
```

---

## Dependencias

| Librería | Uso |
|----------|-----|
| `Flask` | Framework web |
| `marshmallow` | Validación de esquemas |
| `users_bp` | Verificación de existencia de usuarios (`users_db`) |
| `historial_db` | Almacenamiento del historial |


# Prompt Utilizado 
Analiza el código de los archivos @historial_bp.py py @historial_db.py l Basándote en ellos, genera el archivo de documentación historial_documentacion.md.

para hacerlo como mis compañeros, has de seguir la estructura, formato y estilo de @users_documentacion.md y tomar como referencia también @media_documentacion.md 

La documentación debe incluir todo o mas de lo que te encuentres en las referencias que te he marcado, y recuerda has de hacerlo absando en @historial_bp.py y @historial_db.py 