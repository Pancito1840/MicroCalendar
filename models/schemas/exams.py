from pydantic import BaseModel, Field, field_validator
from typing import Literal

class ExamBase(BaseModel):
    attribute: Literal["Examen", "Cuestionario"] = Field(
        ..., description="Debe ser 'Examen' o 'Cuestionario'"
    )
    subject: str = Field(
        ...,
        min_length=1,
        description="Nombre de la asignatura, no puede estar vacío"
    )
    date: str = Field(
        ...,
        pattern=r"^\d{4}-(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)-\d{2}$",
        description="Formato de fecha YYYY-mes-DD, ej: 2026-oct-15"
    )
    time: str = Field(
        ...,
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
        description="Formato de hora HH:MM en 24 horas"
    )

    @field_validator("subject")
    @classmethod
    def validate_subject_is_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("La asignatura no puede estar vacía")
        return value.strip()

class ExamCreate(ExamBase):
    pass

class ExamUpdate(ExamBase):
    pass

class ExamResponse(ExamBase):
    id: int = Field(..., description="Identificador único autoincremental")
