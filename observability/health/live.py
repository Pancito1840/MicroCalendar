from fastapi import APIRouter, status

router = APIRouter(tags=["Observabilidad"])

@router.get("/health/live", status_code=status.HTTP_200_OK)
def liveness_check():
    return {"status", "alive"}
