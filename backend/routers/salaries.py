from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Job
from schemas import SalaryGroup

router = APIRouter(prefix="/api", tags=["salaries"])


@router.get("/salaries", response_model=list[SalaryGroup])
def get_salaries(
    group_by: str = Query("category", pattern="^(category|position_level)$"),
    db: Session = Depends(get_db),
):
    col = Job.category if group_by == "category" else Job.position_level

    rows = (
        db.query(
            col.label("group"),
            func.min(Job.salary_min).label("min_salary"),
            func.avg(Job.avg_salary).label("avg_salary"),
            func.max(Job.salary_max).label("max_salary"),
            func.count().label("count"),
        )
        .group_by(col)
        .order_by(func.avg(Job.avg_salary).desc())
        .all()
    )

    return [
        SalaryGroup(
            group=r.group or "Unknown",
            min_salary=round(r.min_salary, 2),
            avg_salary=round(r.avg_salary, 2),
            max_salary=round(r.max_salary, 2),
            count=r.count,
        )
        for r in rows
    ]
