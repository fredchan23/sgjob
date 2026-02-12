from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Job
from schemas import CategoryCount

router = APIRouter(prefix="/api", tags=["categories"])


@router.get("/categories", response_model=list[CategoryCount])
def get_categories(db: Session = Depends(get_db)):
    rows = (
        db.query(Job.category, func.count().label("count"))
        .group_by(Job.category)
        .order_by(func.count().desc())
        .all()
    )
    return [CategoryCount(category=r.category, count=r.count) for r in rows]
