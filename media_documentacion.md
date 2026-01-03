# Documentación de Endpoints - Medios de Streaming

Esta documentación describe los endpoints disponibles en el módulo de medios de streaming (`media_bp.py`) de la API de Streaming.

**Base URL:** `/medio_de_streaming`

---

## Estructura de Datos

### `medios`

La base de datos de medios se almacena en memoria como un diccionario Python con la siguiente estructura:

```python
medios = {
    1: {
        "pais": "nombre_pais",
        "fecha_de_subida": "YYYY-MM-DD"
    }
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_medio_de_streaming` (clave) | `integer` | Identificador único del medio de streaming |
| `pais` | `string` | País de origen o disponibilidad del medio |
| `fecha_de_subida` | `string` | Fecha en que se subió el medio (formato: YYYY-MM-DD) |

> [!IMPORTANT]
> Los datos se almacenan en memoria, por lo que se pierden al reiniciar el servidor.

---

## Endpoints

### 1. Listar Medios (con Filtros)

**Endpoint:** `GET /medio_de_streaming/`

Devuelve una lista de medios de streaming. Puede devolver todos los medios o filtrar por país, fecha de subida y limitar el número de resultados.

#### Request

**Query Parameters:**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `pais` | `string` | ❌ No | Filtra los medios por nombre de país (case-insensitive) |
| `fecha_subida` | `string` | ❌ No | Filtra los medios por fecha de subida (YYYY-MM-DD) |
| `num_items` | `int` | ❌ No | Limita el número de resultados (solo funciona junto con `fecha_subida`) |

**Ejemplos de URL:**
- Todos: `GET /medio_de_streaming/`
- Por País: `GET /medio_de_streaming/?pais=España`
- Por Fecha: `GET /medio_de_streaming/?fecha_subida=2024-01-15`
- Por Fecha con Límite: `GET /medio_de_streaming/?fecha_subida=2024-01-15&num_items=5`

#### Responses

**✅ Éxito (200):**
```json
{
    "medio_de_streaming": [
        {
            "id_medio_de_streaming": "abc123",
            "medio": {
                "pais": "España",
                "fecha_de_subida": "2024-01-15"
            }
        }
    ]
}
```
*Si no hay filtros, devuelve el diccionario completo de medios.*

**❌ No encontrado (404):**
```json
{
    "error": "No hay medios de streaming en ese país"
}
```
*Ocurre si no hay coincidencias para el filtro aplicado.*

**❌ Error de validación (400):**
```json
{
    "Error": "num_items debe ser entero"
}
```

---

### 2. Obtener Medio por ID (Reproducir)

**Endpoint:** `GET /medio_de_streaming/<id_medio_de_streaming>`

Obtiene la información de un medio específico para reproducirlo.

#### Request

**Parámetros de URL:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id_medio_de_streaming` | `integer` | ID del medio a consultar |

#### Responses

**✅ Éxito (200):**
```json
{
    "medio_de_streaming": {
        "pais": "España",
        "fecha_de_subida": "2024-01-15"
    }
}
```

**❌ Medio no encontrado (404):**
```json
{
    "error": "Medio not found"
}
```

---

### 3. Añadir Medio

**Endpoint:** `POST /medio_de_streaming/anadir_medio`

Añade un nuevo medio de streaming. El ID se envía en el cuerpo JSON, no en la URL.

#### Request

**Body (JSON):**
```json
{
    "id_medio_de_streaming": 1,
    "pais": "España",
    "fecha_de_subida": "2024-01-15"
}
```

**✅ Éxito (201):**
```json
{
    "Mensaje": "Medio de streaming añadido"
}
```

---

### 4. Editar Medio

**Endpoint:** `PUT /medio_de_streaming/<id_medio_de_streaming>`

Modifica los datos de un medio existente.

#### Request

**Body (JSON):**
```json
{
    "id_medio_de_streaming": 1,
    "pais": "Nuevo País",
    "fecha_de_subida": "2024-02-20"
}
```

**✅ Éxito (200):**
```json
{
    "mensaje": "Medio de streaming editado"
}
```

---

### 5. Eliminar Medio

**Endpoint:** `DELETE /medio_de_streaming/<id_medio_de_streaming>`

Elimina un medio de streaming.

#### Responses

**✅ Éxito (200):**
```json
{
    "Mensaje": "Medio de streaming eliminado"
}
```

**❌ Medio no encontrado (404):**
```json
{
    "Error": "Medio no encontrado"
}
```

---

## Esquemas de Validación

### MediaSchema
```python
class MediaSchema(Schema):
    id_medio_de_streaming = fields.Int(required=True)
    pais = fields.Str(required=True)
    fecha_de_subida = fields.Date(required=True)
```