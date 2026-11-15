from fastapi.testclient import TestClient
from main import app
from repository.memory import exam_repository

client = TestClient(app)

def setup_function():
    """
    Se limpia el repositorio en memoria antes de cada test para mantener independencia.
    """
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

def test_create_exam_conflict():
    """Prueba que lance un conflicto (Código 409) al intentar registrar dos exámenes el mismo día"""
    client.post("/exams", json={
        "attribute": "Examen",
        "subject": "Física I",
        "date": "2026-oct-20",
        "time": "09:00"
    })

    response = client.post("/exams", json={
        "attribute": "Cuestionario",
        "subject": "Química General",
        "date": "2026-oct-20",
        "time": "11:00"
    })

    assert response.status_code == 409
    # Ajustado al texto exacto que emite la validación del servicio
    assert "Ya esciste un registro" in response.json()["detail"]

def test_get_exam_by_id_not_found():
    """Prueba que devuelva 404 si se busca un ID que no existe"""
    response = client.get("/exams/999")
    assert response.status_code == 404

def test_list_exams():
    """Prueba listar los exámenes registrados"""
    client.post("/exams", json={
        "attribute": "Examen",
        "subject": "Historia",
        "date": "2026-nov-01",
        "time": "10:00"
    })

    response = client.get("/exams")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["subject"] == "Historia"

def test_health_checks():
    """Prueba las sondas de salud de la Fase 4"""
    response_live = client.get("/health/live")
    assert response_live.status_code == 200

    response_ready = client.get("/health/ready")
    assert response_ready.status_code == 200
