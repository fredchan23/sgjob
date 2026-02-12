from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Job
from schemas import OverviewResponse

router = APIRouter(prefix="/api", tags=["overview"])


@router.get("/overview", response_model=OverviewResponse)
def get_overview(db: Session = Depends(get_db)):
    total_jobs = db.query(func.count(Job.job_post_id)).scalar()
    avg_salary = db.query(func.avg(Job.avg_salary)).scalar() or 0
    total_vacancies = db.query(func.sum(Job.num_vacancies)).scalar() or 0

    top_category = (
        db.query(Job.category, func.count().label("cnt"))
        .group_by(Job.category)
        .order_by(func.count().desc())
        .first()
    )

    date_min = db.query(func.min(Job.posting_date)).scalar()
    date_max = db.query(func.max(Job.posting_date)).scalar()

    return OverviewResponse(
        total_jobs=total_jobs,
        avg_salary=round(avg_salary, 2),
        total_vacancies=total_vacancies,
        top_category=top_category[0] if top_category else "N/A",
        date_min=str(date_min) if date_min else "",
        date_max=str(date_max) if date_max else "",
    )
