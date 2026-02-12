"""
Load cleaned_SGJobData.csv into SQLite database (chunked for memory efficiency).
"""

import pandas as pd
from pathlib import Path
from sqlalchemy import text
from database import engine, Base

CLEANED_CSV = Path(__file__).resolve().parent.parent / "data" / "cleaned_SGJobData.csv"
CHUNK_SIZE = 50_000


def main():
    print("Creating tables...")
    # Import models so they're registered with Base
    import models  # noqa: F401
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    print(f"Loading {CLEANED_CSV} in chunks of {CHUNK_SIZE}...")
    total = 0
    for chunk in pd.read_csv(CLEANED_CSV, chunksize=CHUNK_SIZE, parse_dates=["posting_date", "expiry_date"]):
        # Convert datetime to date strings for SQLite compatibility
        for col in ["posting_date", "expiry_date"]:
            chunk[col] = chunk[col].dt.strftime("%Y-%m-%d")
        chunk.to_sql("jobs", engine, if_exists="append", index=False)
        total += len(chunk)
        print(f"  Loaded {total} rows...")

    print(f"Done. Total rows: {total}")

    # Verify
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM jobs")).scalar()
        print(f"Verified row count in DB: {count}")


if __name__ == "__main__":
    main()
