# Errores y Problemas Detectados en el Proyecto

Este documento lista los errores y problemas encontrados en la API de Streaming.

---

## 🔴 Errores Críticos

*No hay errores críticos pendientes.*

---

## ✅ Errores Corregidos

### ~~1. `media_bp.py` - Rutas duplicadas (GET `/`)~~ ✅ CORREGIDO

Se combinaron las 3 funciones duplicadas (`lista_de_medios_por_pais`, `lista_de_medios_por_fecha`, `obtener_medios`) en una sola función `listar_medios()` que maneja todos los query params.

### ~~2. `media_bp.py` - Método HTTP incorrecto para editar~~ ✅ CORREGIDO

Se cambió el método de DELETE a PUT en la función `editar_medio`.

### ~~3. `media_bp.py` - Falta decorador @ en ruta~~ ✅ CORREGIDO

Se eliminó la función huérfana `medios_por_fecha_limite()` y su lógica se integró en `listar_medios()`.

### ~~4. `media_bp.py` - Typo en variable~~ ✅ CORREGIDO

Se eliminó junto con la función `medios_por_fecha_limite()`.

### ~~5. `media_bp.py` - Método `.lower` sin paréntesis~~ ✅ CORREGIDO

Se corrigió a `.lower()` en la función `listar_medios()`.

### ~~6. `media_bp.py` - Uso incorrecto de `media_bp.get()`~~ ✅ CORREGIDO

Ahora usa correctamente `medios.get(id_medio_de_streaming)`.

### ~~7. Rutas inconsistentes en `backend.py`~~ ✅ CORREGIDO

Se quitaron los prefijos incorrectos de `historial_bp` y `suscripciones_bp`.

### ~~8. `test_api.py` - URLs incorrectas~~ ✅ CORREGIDO

Las URLs ahora son correctas.

### ~~9. `users_bp.py` - Typo en clave de error~~ ✅ CORREGIDO

Se corrigió `"Error:"` a `"Error"` y se añadió el código de estado 400.

---

## 🟡 Errores Menores

### 1. Inconsistencia en nombres de campos

| Archivo | Campo usado | Campo esperado |
|---------|------------|----------------|
| Query param | `fecha_subida` | `fecha_de_subida` |

El schema define `fecha_de_subida` pero el query param usa `fecha_subida`. Esto puede ser intencional para simplificar la URL.

---

## 🟢 Advertencias

### 1. Datos en memoria

Todos los datos se almacenan en memoria (diccionarios Python). Se pierden al reiniciar el servidor.

### 2. `JWT_SECRET_KEY` puede ser `None`

**Archivo:** `backend.py` - Línea 12

```python
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
```

Si la variable de entorno no está definida, será `None` y causará problemas con JWT.

### 3. Endpoints de usuarios exponen contraseñas hasheadas

**Archivo:** `users_bp.py` - Línea 59-61

El endpoint `GET /usuarios/` devuelve todos los usuarios incluyendo los hashes de contraseñas.

---

## Resumen

| Severidad | Cantidad |
|-----------|----------|
| 🔴 Crítico | 0 |
| 🟡 Menor | 1 |
| 🟢 Advertencia | 3 |
| ✅ Corregido | 9 |

---

*Documento actualizado: 2026-01-03*
