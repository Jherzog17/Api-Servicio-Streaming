# Errores y Problemas Detectados en el Proyecto

Este documento lista los errores y problemas encontrados en la API de Streaming.

---

## 🔴 Errores Críticos

### 1. `media_bp.py` - Uso incorrecto de `media_bp.get()`

**Archivo:** `media_bp.py` - Línea 15

```python
data=media_bp.get(id_medio_de_streaming)  # ❌ INCORRECTO
```

**Problema:** `media_bp` es un Blueprint de Flask, no el diccionario de medios. El Blueprint no tiene método `get()`.

**Solución:**
```python
data=medios.get(id_medio_de_streaming)  # ✅ CORRECTO
```

---

### 2. `media_bp.py` - Rutas duplicadas

**Archivo:** `media_bp.py` - Líneas 20-31 y 33-44

```python
@media_bp.route("/", methods=["GET"])
def lista_de_medios_por_pais():
    ...

@media_bp.route("/", methods=["GET"])  # ❌ RUTA DUPLICADA
def lista_de_medios_por_fecha():
    ...
```

**Problema:** Flask solo registrará la primera función. La función `lista_de_medios_por_fecha` nunca se ejecutará.

**Solución:** Combinar ambas funciones en una sola que maneje ambos query params, o usar rutas diferentes.

---

## ✅ Errores Corregidos

### ~~3. Rutas inconsistentes en `backend.py`~~ ✅ CORREGIDO

Se quitaron los prefijos incorrectos de `historial_bp` y `suscripciones_bp`.

### ~~4. `test_api.py` - URLs incorrectas~~ ✅ CORREGIDO

Las URLs ahora son correctas ya que se revirtieron los cambios en `backend.py`.

### ~~5. `users_bp.py` - Typo en clave de error~~ ✅ CORREGIDO

Se corrigió `"Error:"` a `"Error"` y se añadió el código de estado 400.

---

## 🟡 Errores Menores

### 3. `media_bp.py` - Falta código de estado

**Archivo:** `media_bp.py` - Línea 37

```python
return jsonify({'error':'Falta en la cadena de consulta ?fecha_subida=fecha'})  # ❌ Falta status code
```

**Solución:**
```python
return jsonify({'error':'Falta en la cadena de consulta ?fecha_subida=fecha'}), 400  # ✅
```

---

### 4. Inconsistencia en nombres de campos

| Archivo | Campo usado | Campo esperado |
|---------|------------|----------------|
| `media_bp.py` línea 40 | `fecha_subida` | `fecha_de_subida` |

El schema define `fecha_de_subida` pero la búsqueda usa `fecha_subida`.

---

## 🟢 Advertencias

### 5. Datos en memoria

Todos los datos se almacenan en memoria (diccionarios Python). Se pierden al reiniciar el servidor.

### 6. `JWT_SECRET_KEY` puede ser `None`

**Archivo:** `backend.py` - Línea 12

```python
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
```

Si la variable de entorno no está definida, será `None` y causará problemas con JWT.

### 7. Endpoints de usuarios exponen contraseñas hasheadas

**Archivo:** `users_bp.py` - Línea 59-61

El endpoint `GET /usuarios/` devuelve todos los usuarios incluyendo los hashes de contraseñas.

---

## Resumen

| Severidad | Cantidad |
|-----------|----------|
| 🔴 Crítico | 2 |
| 🟡 Menor | 2 |
| 🟢 Advertencia | 3 |
| ✅ Corregido | 3 |

---

*Documento generado con IA - Actualizado después de correcciones del usuario*
