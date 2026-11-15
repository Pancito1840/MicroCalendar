from fastapi import APIRouter, status

router = APIRouter(tags=["Observabilidad"])

@router.get("/health/ready", status_code=status.HTTP_200_OK)
def readiness_check():
    return {"status", "ready"}
