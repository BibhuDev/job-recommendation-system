
import math


def precision_at_k(results, relevant_ids: set[int], k: int) -> float:
    if k <= 0:
        return 0.0

    retrieved_ids = [job.id for job in results[:k]]
    relevant_count = sum(
        1 for job_id in retrieved_ids if job_id in relevant_ids
    )

    return relevant_count / k


def recall_at_k(results, relevant_ids: set[int], k: int) -> float:
    if not relevant_ids or k <= 0:
        return 0.0

    retrieved_ids = {job.id for job in results[:k]}
    relevant_count = len(retrieved_ids & relevant_ids)

    return relevant_count / len(relevant_ids)


def ndcg_at_k(results, relevant_ids: set[int], k: int) -> float:
    if not relevant_ids or k <= 0:
        return 0.0

    retrieved_ids = [job.id for job in results[:k]]

    dcg = sum(
        1 / math.log2(rank + 1)
        for rank, job_id in enumerate(retrieved_ids, start=1)
        if job_id in relevant_ids
    )

    ideal_relevant_count = min(len(relevant_ids), k)

    idcg = sum(
        1 / math.log2(rank + 1)
        for rank in range(1, ideal_relevant_count + 1)
    )

    return dcg / idcg if idcg else 0.0


def evaluate_method(search_function, db, test_queries, k=3):
    results = []

    for query, relevant_ids in test_queries.items():
        jobs = search_function(
            db,
            query,
            skip=0,
            limit=k
        )

        results.append({
            "query": query,
            "precision": precision_at_k(jobs, relevant_ids, k),
            "recall": recall_at_k(jobs, relevant_ids, k),
            "ndcg": ndcg_at_k(jobs, relevant_ids, k)
        })

    count = len(results)

    return {
        "precision": sum(r["precision"] for r in results) / count,
        "recall": sum(r["recall"] for r in results) / count,
        "ndcg": sum(r["ndcg"] for r in results) / count,
        "details": results
    }
