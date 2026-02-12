from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, String
from database import get_db
from models import Job
from schemas import TrendPoint

router = APIRouter(prefix="/api", tags=["trends"])


@router.get("/trends", response_model=list[TrendPoint])
def get_trends(
    interval: str = Query("month", pattern="^(month|year)$"),
    db: Session = Depends(get_db),
):
    year_col = extract("year", Job.posting_date)
    month_col = extract("month", Job.posting_date)

    if interval == "month":
        period_expr = func.printf("%04d-%02d", year_col, month_col)
        rows = (
            db.query(
                period_expr.label("period"),
                func.count().label("count"),
            )
            .group_by(period_expr)
            .order_by(period_expr)
            .all()
        )
    else:
        rows = (
            db.query(
                func.cast(year_col, String).label("period"),
                func.count().label("count"),
            )
            .group_by(year_col)
            .order_by(year_col)
            .all()
        )

    return [TrendPoint(period=r.period, count=r.count) for r in rows]
