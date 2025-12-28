# Documentación de Endpoints - Medios de Streaming

Esta documentación describe los endpoints disponibles en el módulo de medios de streaming (`media_bp.py`) de la API de Streaming.

**Base URL:** `/medio_de_streaming`

---

## Estructura de Datos

### `medios`

La base de datos de medios se almacena en memoria como un diccionario Python con la siguiente estructura:

```python
medios = {
    "id_medio_de_streaming": {
        "pais": "nombre_pais",
        "fecha_de_subida": "YYYY-MM-DD"
    }
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_medio_de_streaming` (clave) | `string` | Identificador único del medio de streaming |
| `pais` | `string` | País de origen o disponibilidad del medio |
| `fecha_de_subida` | `date` | Fecha en que se subió el medio (formato: YYYY-MM-DD) |

> [!IMPORTANT]
> Los datos se almacenan en memoria, por lo que se pierden al reiniciar el servidor.

---

## Endpoints

### 1. Reproducir Medio de Streaming

**Endpoint:** `GET /medio_de_streaming/<id_medio_de_streaming>`

Obtiene la información de un medio de streaming específico por su ID.

#### Request

**Parámetros de URL:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id_medio_de_streaming` | `string` | ID del medio de streaming a consultar |

No requiere body.

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

### 2. Lista de Medios por País

**Endpoint:** `GET /medio_de_streaming/?pais=<nombre_pais>`

Devuelve todos los medios de streaming disponibles en un país específico.

#### Request

**Query Parameters:**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `pais` | `string` | ✅ Sí | Nombre del país para filtrar los medios |

**Ejemplo de URL:**
```
GET /medio_de_streaming/?pais=España
```

No requiere body.

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
        },
        {
            "id_medio_de_streaming": "def456",
            "medio": {
                "pais": "España",
                "fecha_de_subida": "2024-02-20"
            }
        }
    ]
}
```

**❌ Falta parámetro país (404):**
```json
{
    "error": "Falta en la cadena de consulta ?pais=nombre_pais"
}
```

**❌ No hay medios en ese país (404):**
```json
{
    "error": "No hay medios de streaming en ese pais"
}
```

> [!NOTE]
> La búsqueda por país es case-insensitive (no distingue mayúsculas/minúsculas).

---

### 3. Lista de Medios por Fecha de Subida

**Endpoint:** `GET /medio_de_streaming/?fecha_subida=<fecha>`

Devuelve todos los medios de streaming subidos en una fecha específica.

#### Request

**Query Parameters:**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `fecha_subida` | `string` | ✅ Sí | Fecha de subida para filtrar los medios |

**Ejemplo de URL:**
```
GET /medio_de_streaming/?fecha_subida=2024-01-15
```

No requiere body.

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

**❌ Falta parámetro fecha_subida:**
```json
{
    "error": "Falta en la cadena de consulta ?fecha_subida=fecha"
}
```

**❌ No hay medios con esa fecha (404):**
```json
{
    "error": "No hay medios de streaming con esa fecha de subida"
}
```

> [!WARNING]
> Actualmente, los endpoints de lista por país y lista por fecha están duplicados con la misma ruta (`GET /`). Esto puede causar conflictos ya que Flask solo ejecutará el primer endpoint registrado.

---

## Esquemas de Validación

El módulo utiliza **Marshmallow** para validar los datos de entrada:

### MediaSchema
```python
class MediaSchema(Schema):
    id_medio_de_streaming = fields.Int(required=True)
    pais = fields.Str(required=True)
    fecha_de_subida = fields.Date(required=True)
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id_medio_de_streaming` | `integer` | ✅ Sí | ID del medio de streaming |
| `pais` | `string` | ✅ Sí | País de origen o disponibilidad |
| `fecha_de_subida` | `date` | ✅ Sí | Fecha de subida del medio |

---

## Dependencias

| Librería | Uso |
|----------|-----|
| `Flask` | Framework web |
| `marshmallow` | Validación de esquemas |
| `media_db` | Almacenamiento de datos de medios |

---

## Notas Adicionales

> [!CAUTION]
> Se detectó un posible error en el código: en la función `reproducir_medio_de_streaming`, se utiliza `media_bp.get()` en lugar de `medios.get()`. Esto causará un error ya que `media_bp` es un Blueprint y no tiene el método `get()`.

Prompt utilizado 

Crea un documneto md como el de @users_documentacion.md pero para @media_bp.py
 