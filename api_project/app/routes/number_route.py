from fastapi import APIRouter, HTTPException, Query
from app.models.number import NumbersSet

router = APIRouter()

numbers_set = NumbersSet()

@router.post("/extract/")
def extract_number(number: int = Query(..., ge=1, le=100)):
    try:
        numbers_set.extract(number)
        return {"message": f"Número {number} extraído correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/missing/")
def get_missing_number():
    missing = numbers_set.find_missing()
    return {"missing_number": missing}
