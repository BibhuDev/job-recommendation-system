from pathlib import Path

from backend.app.db.database import SessionLocal
from backend.app.services.job_ingestion import import_jobs_from_csv


def main():
    project_root = Path(__file__).resolve().parents[2]
    csv_path = project_root / "data" / "jobs.csv"

    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return

    db = SessionLocal()

    try:
        result = import_jobs_from_csv(db, str(csv_path))

        print("\nJob ingestion completed!")
        print(f"Inserted: {result['inserted']}")
        print(f"Skipped: {result['skipped']}")
        print(f"Errors: {len(result['errors'])}")

        for error in result["errors"]:
            print(f"Row {error['row']}: {error['error']}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
