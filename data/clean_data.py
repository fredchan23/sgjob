"""
Cleaning pipeline for SGJobData.csv → cleaned_SGJobData.csv

Decisions documented in data/eda.ipynb.
"""

import json
import pandas as pd
from pathlib import Path

RAW_CSV = Path(__file__).resolve().parent.parent / "SGJobData.csv"
OUT_CSV = Path(__file__).resolve().parent / "cleaned_SGJobData.csv"


def parse_primary_category(cat_str: str) -> str | None:
    try:
        cats = json.loads(cat_str)
        return cats[0]["category"] if cats else None
    except (json.JSONDecodeError, TypeError, KeyError, IndexError):
        return None


def clean(df: pd.DataFrame) -> pd.DataFrame:
    print(f"Raw rows: {len(df)}")

    # 1. Drop duplicates by job post ID
    df = df.drop_duplicates(subset="metadata_jobPostId", keep="last").copy()
    print(f"After dedup: {len(df)}")

    # 2. Parse categories JSON → primary category
    df["category"] = df["categories"].apply(parse_primary_category)
    df = df.dropna(subset=["category"])
    print(f"After category parse: {len(df)}")

    # 3. Normalize salary
    df = df[~((df["salary_minimum"] == 0) & (df["salary_maximum"] == 0))].copy()
    print(f"After dropping zero salary: {len(df)}")

    # Cap outliers at 99th percentile
    p99_min = df["salary_minimum"].quantile(0.99)
    p99_max = df["salary_maximum"].quantile(0.99)
    df["salary_minimum"] = df["salary_minimum"].clip(upper=p99_min)
    df["salary_maximum"] = df["salary_maximum"].clip(upper=p99_max)

    # Ensure min <= max
    mask = df["salary_minimum"] > df["salary_maximum"]
    df.loc[mask, ["salary_minimum", "salary_maximum"]] = (
        df.loc[mask, ["salary_maximum", "salary_minimum"]].values
    )

    # Recompute average salary after clipping
    df["average_salary"] = (df["salary_minimum"] + df["salary_maximum"]) / 2

    # 4. Parse dates, drop invalid
    df["posting_date"] = pd.to_datetime(df["metadata_newPostingDate"], errors="coerce")
    df["expiry_date"] = pd.to_datetime(df["metadata_expiryDate"], errors="coerce")
    df = df.dropna(subset=["posting_date"])
    print(f"After date parse: {len(df)}")

    # 5. Fill missing values
    df["minimumYearsExperience"] = df["minimumYearsExperience"].fillna(0).astype(int)
    df["numberOfVacancies"] = df["numberOfVacancies"].fillna(1).astype(int)

    # 6. Standardize company names
    df["postedCompany_name"] = df["postedCompany_name"].str.strip().str.upper()

    # 7. Rename columns to clean snake_case
    df = df.rename(columns={
        "metadata_jobPostId": "job_post_id",
        "title": "title",
        "employmentTypes": "employment_type",
        "postedCompany_name": "company",
        "salary_minimum": "salary_min",
        "salary_maximum": "salary_max",
        "average_salary": "avg_salary",
        "salary_type": "salary_type",
        "positionLevels": "position_level",
        "minimumYearsExperience": "min_years_exp",
        "numberOfVacancies": "num_vacancies",
        "metadata_totalNumberJobApplication": "num_applications",
        "metadata_totalNumberOfView": "num_views",
        "status_jobStatus": "status",
    })

    # Select final columns
    cols = [
        "job_post_id", "title", "category", "employment_type", "company",
        "salary_min", "salary_max", "avg_salary", "salary_type",
        "position_level", "min_years_exp", "num_vacancies",
        "num_applications", "num_views", "posting_date", "expiry_date", "status",
    ]
    df = df[cols]
    print(f"Final rows: {len(df)}")
    return df


def main():
    print(f"Reading {RAW_CSV} ...")
    df = pd.read_csv(RAW_CSV, low_memory=False)
    df = clean(df)
    df.to_csv(OUT_CSV, index=False)
    print(f"Saved cleaned data to {OUT_CSV}")


if __name__ == "__main__":
    main()
