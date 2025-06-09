from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.services import QueryService, MutationService

router = APIRouter()


# Department routes
@router.get("/departments")
async def get_departments(db: Session = Depends(get_db)):
    return QueryService(db).get_all_departments()


@router.post("/departments")
async def create_department(department_data: dict, db: Session = Depends(get_db)):
    return MutationService.create_department(db, department_data)


@router.delete("/departments/{department_id}")
async def delete_department(department_id: int, db: Session = Depends(get_db)):
    return MutationService.delete_department(db, department_id)


# Part routes
@router.get("/parts")
async def get_parts(db: Session = Depends(get_db)):
    return QueryService(db).get_all_parts()


@router.post("/parts")
async def create_part(part_data: dict, db: Session = Depends(get_db)):
    return MutationService.create_part(db, part_data)


# Quality routes
@router.get("/quality/{part_id}")
async def get_quality(part_id: int, db: Session = Depends(get_db)):
    return QueryService(db).get_quality_by_part(part_id)
