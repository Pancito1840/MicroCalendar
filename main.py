from fastapi import FastAPI
from routers.exam_router import router as exam_router

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="Microservicio de Horarios de Exámenes",
    description="API CRUD en memoria desarrollada con FastAPI y Docker",
    version="1.0.0"
)

# Conectamos el router de exámenes
app.include_router(exam_router)

@app.get("/", tags=["Raíz"])
def read_root():
    return {
        "message": "Bienvenido al Microservicio de Horarios de Exámenes",
        "docs": "/docs"
    }
