from typing import Dict, List, Optional

class ExamRepository:

    """
    Repositorio en memoria.
    Nota de concurrencia: Al no utilizar una base de datos real,
    este microservicio está documentado para ejecutarse con un solo worker
    de Uvicorn para evitar condiciones de carrera en el diccionario.
    """
    def __init__(self):
        # Diccionario principal: { id: { datos_del_examen } }
        self._storage: Dict[int, dict] = {}
        # Contador para generar IDs autoincrementales
        self._id_counter: int = 0

    def create(self, exam_data: dict) -> dict:
        self._id_counter += 1
        exam_id = self._id_counter

        # Guardamos el id junto con los datos recibidos
        new_exam = {"id": exam_id, **exam_data}
        self._storage[exam_id] = new_exam
        return new_exam

    def get_by_id(self, exam_id: int) -> Optional[dict]:
        return self._storage.get(exam_id)

    def get_all(self) -> List[dict]:
        return list(self._storage.values())

    def get_by_date(self, date: str) -> List[dict]:
        # Filtra los exámenes que coincidan con la fecha especificada
        return [exam for exam in self._storage.values() if exam["date"] == date]

    def update(self, exam_id: int, exam_data: dict) -> Optional[dict]:
        if exam_id not in self._storage:
            return None

        updated_exam = {"id": exam_id, **exam_data}
        self._storage[exam_id] = updated_exam
        return updated_exam

    def delete(self, exam_id: int) -> bool:
        if exam_id not in self._storage:
            return False
        del self._storage[exam_id]
        return True

# Instancia global del repositorio para ser usada en la aplicación
exam_repository = ExamRepository()
