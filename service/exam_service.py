from typing import List, Optional
from repository.memory import exam_repository

class ExamService:
    def create_exam(self, exam_data: dict) -> dict:
        requested_date = exam_data.get("date")
        requested_time = exam_data.get("time")

        if not requested_date or not requested_time:
            raise ValueError("La fecha y la hora son obligatorias.")

        # Obtenemos los exámenes de ese día
        existing_exams = exam_repository.get_by_date(requested_date)

        # Verificamos si ya existe uno a la misma hora exacta
        for exam in existing_exams:
            if exam.get("time") == requested_time:
                raise ValueError(f"Ya existe un registro el {requested_date} a las {requested_time}")

        return exam_repository.create(exam_data)

    def get_all_exams(self, date: Optional[str] = None) -> List[dict]:
        if date:
            return exam_repository.get_by_date(date)
        return exam_repository.get_all()

    def get_exam_by_id(self, exam_id: int) -> Optional[dict]:
        return exam_repository.get_by_id(exam_id)

    def update_exam(self, exam_id: int, exam_data: dict) -> Optional[dict]:
        existing = exam_repository.get_by_id(exam_id)
        if not existing:
            return None
        return exam_repository.update(exam_id, exam_data)

    def delete_exam(self, exam_id: int) -> bool:
        return exam_repository.delete(exam_id)

exam_service = ExamService()
