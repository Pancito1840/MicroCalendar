from fastapi.testclient import TestClient
from main import app
from repository.memory import exam_repository

client = TestClient(app)

def setup_function():
    """Limpia el repositorio en memoria antes de cada test."""
    exam_repository._storage.clear()
    exam_repository._id_counter = 0

def test_create_exam_success():
    """Prueba la creación exitosa de un examen (Código 201)"""
    response = client.post("/exams", json={
        "attribute": "Examen",
        "subject": "Matemáticas Avanzadas",
        "date": "2026-oct-15",
        "time": "14:30"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["subject"] == "Matemáticas Avanzadas"
    assert data["attribute"] == "Examen"

def test_create_exam_same_day_different_time_success():
    """Prueba que se puedan crear varios exámenes el mismo día a distintas horas (Código 201)"""
    # Primer examen a las 09:00
    res1 = client.post("/exams", json={
        "attribute": "Examen",
        "subject": "Física I",
        "date": "2026-oct-20",
        "time": "09:00"
    })
    assert res1.status_code == 201

    # Segundo examen el mismo día pero a las 11:00 (Debe pasar con éxito)
    res2 = client.post("/exams", json={
        "attribute": "Cuestionario",
        "subject": "Química General",
        "date": "2026-oct-20",
        "time": "11:00"
    })
    assert res2.status_code == 201

def test_create_exam_conflict():
    """Prueba que lance conflicto (409) si se intenta registrar un examen el mismo día y misma hora"""
    # Creamos un examen inicial
    client.post("/exams", json={
        "attribute": "Examen",
        "subject": "Historia",
        "date": "2026-oct-25",
        "time": "10:00"
    })

    # Intentamos crear otro examen en la misma fecha Y la misma hora exacta
    response = client.post("/exams", json={
        "attribute": "Cuestionario",
        "subject": "Geografía",
        "date": "2026-oct-25",
        "time": "10:00"
    })

    assert response.status_code == 409
    assert "Ya existe un registro" in response.json()["detail"]

def test_get_exam_by_id_not_found():
    """Prueba que devuelva 404 si se busca un ID que no existe"""
    response = client.get("/exams/999")
    assert response.status_code == 404

def test_list_exams():
    """Prueba listar los exámenes registrados"""
    client.post("/exams", json={
        "attribute": "Examen",
        "subject": "Literatura",
        "date": "2026-nov-01",
        "time": "10:00"
    })

    response = client.get("/exams")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["subject"] == "Literatura"

def test_health_checks():
    """Prueba las sondas de salud de la Fase 4"""
    response_live = client.get("/health/live")
    assert response_live.status_code == 200

    response_ready = client.get("/health/ready")
    assert response_ready.status_code == 200
