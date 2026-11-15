# Microservicio de Horarios de Exámenes y Cuestionarios

Microservicio desarrollado en **FastAPI** para la gestión de un calendario académico. Funciona de manera ligera y rápida utilizando almacenamiento temporal en memoria RAM, validaciones estrictas con Pydantic, observabilidad mediante sondas de salud y métricas integradas para Prometheus.

---

## Características Principales
- **CRUD completo** para la gestión de exámenes y cuestionarios.
- **Validación de reglas de negocio:** Restricción estricta de conflicto (código `409`) si se intenta registrar un examen o cuestionario en la misma fecha y hora exacta.
- **Formato de fechas estricto:** Fechas en formato `YYYY-mes-DD` (mes abreviado, ej. `2026-oct-15`) y horas en formato de 24 horas `HH:MM`.
- **Sondas de Salud (Health Checks):** Endpoints separados para verificar el estado vital (`/health/live`) y de disponibilidad (`/health/ready`).
- **Métricas Prometheus:** Exposición automática de métricas de rendimiento en `/metrics`.
- **Contenedorización optimizada:** Dockerfile con imagen base ligera, capas cacheadas, usuario sin privilegios y un único *worker* de Uvicorn (`--workers 1`) para garantizar la persistencia coherente en memoria RAM.

---

## Limitación Importante (Datos en Memoria)
Este microservicio **no utiliza una base de datos persistente (SQL/NoSQL)**; todo el almacenamiento se realiza directamente en la memoria RAM del proceso. 
* **Consecuencia:** Si el contenedor se detiene, se reinicia o la aplicación se apaga, **todos los registros almacenados se perderán**.

---

## Cómo Ejecutar Localmente (Sin Docker)

1. **Crear y activar el entorno virtual:**
   ```bash
   python3 -m venv microservicio
   source microservicio/bin/activate
2. **Instalar dependencias**
pip install -r requirements.txt
3.  **Ejecutar la aplicacion con uvicorn**
uvicorn main:app --reload --workers 1
(La API estará disponible en http://localhost:8000 y la documentación interactiva en http://localhost:8000/docs.)
4. **Ejecutar pruebas automatizadas
python -m pytest -v

--
## Ejecutar con docker
1. **Construir la imagen**
docker build -t microservicio-calendario .
2. **Ejecutar el contenedor**
docker run -d -p 8000:8000 --name calendario-app microservicio-calendario

Lista de endpoints y ejemplos de uso
Crear un Examen o Cuestionario
Método: POST

Ruta: /exams

Cuerpo (JSON): 

{
  "attribute": "Examen",
  "subject": "Matemáticas Avanzadas",
  "date": "2026-oct-15",
  "time": "14:30"
}

Respuesta Exitosa: 201 Created

------------------------------

Listar Todos los Registros (con filtro opcional por fecha)

Método: GET

Ruta: /exams o /exams?date=2026-oct-15

Respuesta Exitosa: 200 OK

------------------------------

Crear un Examen o Cuestionario

Método: GET

Ruta: /exams/{id}

Respuesta Exitosa: 200 OK

------------------------------

Actualizar un Registro

Método: PUT

Ruta: /exams/{id}

Cuerpo (JSON): Campos a modificar.

------------------------------

Eliminar un Registro

Método: DELETE

Ruta: /exams/{id}

Respuesta Exitosa: 200 OK

------------------------------

Sondas de Salud y Métricas

GET /health/live — Comprueba si el proceso está vivo.

GET /health/ready — Comprueba si está listo para recibir tráfico.

GET /metrics — Expone las métricas técnicas en formato Prometheus.
