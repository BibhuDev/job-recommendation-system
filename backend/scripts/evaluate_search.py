
from backend.app.db.database import SessionLocal

from backend.app.services.search_service import (
    bm25_search,
    semantic_search,
    hybrid_search
)

from backend.app.services.evaluation_services import evaluate_method


# Relevance labels based on the five jobs in our database.
# These labels are manually assigned for this demonstration.
TEST_QUERIES = {
    "Python backend API development": {1},
    "building interactive web interfaces": {2},
    "AI predictive modeling": {3},
    "Java enterprise applications": {4},
    "data analysis and visualization": {5}
}

SEARCH_METHODS = {
    "BM25": bm25_search,
    "Semantic": semantic_search,
    "Hybrid": hybrid_search
}


def main():
    db = SessionLocal()

    try:
        print("\nCAREERAI SEARCH EVALUATION")
        print("=" * 60)

        for method_name, search_function in SEARCH_METHODS.items():
            metrics = evaluate_method(
                search_function,
                db,
                TEST_QUERIES,
                k=3
            )

            print(f"\n{method_name} SEARCH")
            print("-" * 40)

            print(f"Precision@3: {metrics['precision']:.4f}")
            print(f"Recall@3:    {metrics['recall']:.4f}")
            print(f"NDCG@3:      {metrics['ndcg']:.4f}")

        print("\nEvaluation completed.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
