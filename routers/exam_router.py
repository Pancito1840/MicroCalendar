from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query
from models.schemas.exams import ExamCreate, ExamUpdate, ExamResponse
from service.exam_service import exam_service

# Creamos el router con un prefijo y etiquetas para la documentación de Swagger
router = APIRouter(prefix="/exams", tags=["Exámenes"])

@router.post("", response_model=ExamResponse, status_code=status.HTTP_201_CREATED)
def create_exam(exam: ExamCreate):
    """
    Crear un examen (responde 201).
    Valida conflictos de fecha (409) y errores de validación (422).
    """
    try:
        # Convertimos el modelo Pydantic a diccionario para pasarlo al servicio
        return exam_service.create_exam(exam.model_dump())
    except ValueError as e:
        # Si la regla de negocio detecta un conflicto por fecha repetida
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.get("", response_model=List[ExamResponse], status_code=status.HTTP_200_OK)
def list_exams(date: Optional[str] = Query(None, description="Filtrar por fecha YYYY-mes-DD")):
    """
    Listar todos los exámenes o filtrar por un día específico (?date=YYYY-mes-DD).
    """
    return exam_service.get_all_exams(date)

@router.get("/{exam_id}", response_model=ExamResponse, status_code=status.HTTP_200_OK)
def get_exam(exam_id: int):
    """
    Consultar un examen específico por su ID. Devuelve 404 si no existe.
    """
    exam = exam_service.get_exam_by_id(exam_id)
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el examen con ID {exam_id}"
        )
    return exam

@router.put("/{exam_id}", response_model=ExamResponse, status_code=status.HTTP_200_OK)
def update_exam(exam_id: int, exam: ExamUpdate):
    """
    Actualizar completo un examen existente por su ID. Devuelve 404 si no existe.
    """
    updated = exam_service.update_exam(exam_id, exam.model_dump())
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede actualizar. No existe el examen con ID {exam_id}"
        )
    return updated

@router.delete("/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exam(exam_id: int):
    """
    Eliminar un examen por su ID (responde 204 sin contenido). Devuelve 404 si no existe.
    """
    deleted = exam_service.delete_exam(exam_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede eliminar. No existe el examen con ID {exam_id}"
        )
    return None
