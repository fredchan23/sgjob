from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Job
from schemas import CompanyRow

router = APIRouter(prefix="/api", tags=["companies"])


@router.get("/companies", response_model=list[CompanyRow])
def get_companies(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(
            Job.company,
            func.count().label("job_count"),
            func.avg(Job.avg_salary).label("avg_salary"),
        )
        .group_by(Job.company)
        .order_by(func.count().desc())
        .limit(limit)
        .all()
    )
    return [
        CompanyRow(
            company=r.company,
            job_count=r.job_count,
            avg_salary=round(r.avg_salary, 2),
        )
        for r in rows
    ]
