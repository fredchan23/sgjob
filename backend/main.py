from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import overview, salaries, categories, companies, trends

app = FastAPI(title="SG Job Data API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(overview.router)
app.include_router(salaries.router)
app.include_router(categories.router)
app.include_router(companies.router)
app.include_router(trends.router)


@app.get("/")
def root():
    return {"message": "SG Job Data API"}
