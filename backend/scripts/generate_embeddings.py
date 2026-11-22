
from backend.app.db.database import SessionLocal
from backend.app.services.embedding_service import generate_job_embeddings


def main():
    db = SessionLocal()

    try:
        generate_job_embeddings(db)
    except Exception as error:
        db.rollback()
        print(f"Embedding generation failed: {error}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
