from pydantic import BaseModel


class OverviewResponse(BaseModel):
    total_jobs: int
    avg_salary: float
    total_vacancies: int
    top_category: str
    date_min: str
    date_max: str


class SalaryGroup(BaseModel):
    group: str
    min_salary: float
    avg_salary: float
    max_salary: float
    count: int


class CategoryCount(BaseModel):
    category: str
    count: int


class CompanyRow(BaseModel):
    company: str
    job_count: int
    avg_salary: float


class TrendPoint(BaseModel):
    period: str
    count: int
