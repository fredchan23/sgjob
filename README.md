# SG Job Data Analysis Dashboard

Full-stack data analysis application for ~1M Singapore job listings from MyCareersFuture. Features a Python/FastAPI backend with SQLite and a React/Recharts frontend dashboard.

## Screenshots

### Overview
![Overview](https://github.com/user-attachments/assets/placeholder-overview)

KPI cards showing total jobs (1,044,597), average salary ($4,634 SGD), total vacancies, top category, and date range.

### Salaries
Salary distribution (min/avg/max) grouped by category or position level.

### Categories
Job count per category — Admin/Secretarial, Engineering, and IT lead.

### Companies
Top 20 companies ranked by job count with average salary.

### Trends
Monthly job posting volume from Feb 2023 to May 2024.

## Project Structure

```
sgjob/
├── data/
│   ├── eda.ipynb              # Exploratory data analysis notebook
│   ├── eda_executed.ipynb     # EDA with outputs
│   └── clean_data.py          # Cleaning pipeline
├── backend/
│   ├── main.py                # FastAPI app
│   ├── database.py            # SQLite + SQLAlchemy setup
│   ├── models.py              # ORM models
│   ├── schemas.py             # Pydantic response schemas
│   ├── load_data.py           # CSV → SQLite loader
│   └── routers/               # API endpoints
│       ├── overview.py        # GET /api/overview
│       ├── salaries.py        # GET /api/salaries
│       ├── categories.py      # GET /api/categories
│       ├── companies.py       # GET /api/companies
│       └── trends.py          # GET /api/trends
└── frontend/
    └── src/
        ├── App.jsx            # Layout + tab navigation
        ├── api.js             # Fetch helpers
        └── components/        # Overview, SalaryChart, CategoryChart,
                               # CompanyTable, TrendsChart
```

## Data Pipeline

```
SGJobData.csv → clean_data.py → cleaned_SGJobData.csv → load_data.py → sgjob.db
```

The cleaning script:
- Drops duplicates by job post ID
- Parses category JSON → extracts primary category
- Removes zero-salary rows, caps outliers at 99th percentile
- Parses and validates dates
- Standardizes company names
- Outputs 1,044,597 cleaned rows

## Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- `SGJobData.csv` in the project root

### Backend

```bash
pip install -r backend/requirements.txt

# Clean raw data
cd data
python clean_data.py

# Load into SQLite
cd ../backend
python load_data.py

# Start API server
uvicorn main:app --reload
```

API docs available at http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard available at http://localhost:5173

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/overview` | Total jobs, avg salary, total vacancies, top category, date range |
| `GET /api/salaries?group_by=category` | Salary stats grouped by category or position_level |
| `GET /api/categories` | Job count per category, sorted descending |
| `GET /api/companies?limit=20` | Top companies by job count with avg salary |
| `GET /api/trends?interval=month` | Job posting counts over time |

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, SQLite, Pandas
- **Frontend**: React 18, Vite, Tailwind CSS, Recharts
- **Data**: Jupyter, Matplotlib, Seaborn
