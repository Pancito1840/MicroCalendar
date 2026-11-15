from typing import List, Optional
from repository.memory import exam_repository

class ExamService:
    def create_exam(self, exam_data: dict) -> dict:
        """
        Regla de negocio para crear un examen:
        Verifica si ya existe un examen en la misma fecha para prevenir conflictos.
        """
        requested_date = exam_data.get("date")

        if not requested_date:
            raise ValueError("Fecha invalida")

        # Consultamos si ya hay exámenes en esa fecha exacta
        existing_exams = exam_repository.get_by_date(requested_date)

        if existing_exams:
            #si existe un examen ya creado lanza un mensaje de conflicto
            raise ValueError(f"Ya esciste un registro el {requested_date}")
            #Si no hay conflicto se crea el registro
        return exam_repository.create(exam_data)

    def get_all_exams(self, date: Optional[str] = None) -> List[dict]:
        """
        Lista todos los exámenes o los filtra por fecha si se proporciona el parámetro.
        """
        if date:
            return exam_repository.get_by_date(date)
        return exam_repository.get_all()

    def get_exam_by_id(self, exam_id: int) -> Optional[dict]:
        """
        Busca un examen por su ID. Retorna None si no existe.
        """
        return exam_repository.get_by_id(exam_id)

    def update_exam(self, exam_id: int, exam_data: dict) -> Optional[dict]:
        """
        Actualiza un examen existente. Retorna None si el ID no se encuentra.
        """
        #verificacion si el examen existe
        existing = exam_repository.get_by_id(exam_id)
        if not existing:
            return None

        return exam_repository.update(exam_id, exam_data)
    def delete_exam(self, exam_id: int) -> bool:
        """
        Elimina un examen por su ID. Retorna True si se borró o False si no existía.
        """
        return exam_repository.delete(exam_id)

exam_service = ExamService()
