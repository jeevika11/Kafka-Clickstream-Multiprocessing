
from collections import Counter
from multiprocessing import Queue
from typing import Any


def aggregate_results(result_queue: Queue, worker_count: int) -> dict[str, Any]:
    """
    Collect worker summaries and combine their counts.

    Each worker sends one dictionary containing event and page counts.
    A None message signals that a worker has finished.
    """
    event_totals = Counter()
    page_totals = Counter()
    total_events = 0
    invalid_events = 0
    finished_workers = 0

    while finished_workers < worker_count:
        result = result_queue.get()

        if result is None:
            finished_workers += 1
            continue

        event_totals.update(result.get("event_types", {}))
        page_totals.update(result.get("pages", {}))
        total_events += result.get("total_events", 0)
        invalid_events += result.get("invalid_events", 0)

    return {
        "total_events": total_events,
        "invalid_events": invalid_events,
        "event_types": dict(event_totals),
        "pages": dict(page_totals),
        "workers_finished": finished_workers,
    }


def print_summary(summary: dict[str, Any]) -> None:
    """Print the combined clickstream report."""
    print("\n" + "=" * 50)
    print("CLICKSTREAM AGGREGATION SUMMARY")
    print("=" * 50)
    print("Valid events   :", summary["total_events"])
    print("Invalid events :", summary["invalid_events"])
    print("Workers finished:", summary["workers_finished"])

    print("\nEvent type counts:")
    for event_type, count in sorted(summary["event_types"].items()):
        print(f"  {event_type:<15}: {count}")

    print("\nPage counts:")
    for page, count in sorted(summary["pages"].items()):
        print(f"  {page:<15}: {count}")

    print("=" * 50)


if __name__ == "__main__":
    # Simple standalone demonstration with two worker summaries.
    demo_queue = Queue()
    demo_queue.put({
        "total_events": 3,
        "invalid_events": 0,
        "event_types": {"click": 2, "page_view": 1},
        "pages": {"/": 2, "/products": 1},
    })
    demo_queue.put({
        "total_events": 2,
        "invalid_events": 0,
        "event_types": {"purchase": 1, "click": 1},
        "pages": {"/checkout": 1, "/": 1},
    })
    demo_queue.put(None)
    demo_queue.put(None)

    print_summary(aggregate_results(demo_queue, worker_count=2))
    demo_queue.close()
