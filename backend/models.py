from sqlalchemy import Column, String, Integer, Float, Date, Index
from database import Base


class Job(Base):
    __tablename__ = "jobs"

    job_post_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    employment_type = Column(String)
    company = Column(String, nullable=False, index=True)
    salary_min = Column(Float)
    salary_max = Column(Float)
    avg_salary = Column(Float, index=True)
    salary_type = Column(String)
    position_level = Column(String)
    min_years_exp = Column(Integer)
    num_vacancies = Column(Integer)
    num_applications = Column(Integer)
    num_views = Column(Integer)
    posting_date = Column(Date, index=True)
    expiry_date = Column(Date)
    status = Column(String)
