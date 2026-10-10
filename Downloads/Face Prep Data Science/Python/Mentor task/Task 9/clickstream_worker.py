
import json
from collections import Counter


def process_event(event):
    """Validate a clickstream event and extract aggregation fields."""
    required_fields = {
        "event_id",
        "user_id",
        "event_type",
        "page",
        "timestamp",
    }

    if not isinstance(event, dict):
        raise ValueError("Event must be a JSON object")

    missing = required_fields.difference(event)
    if missing:
        raise ValueError(f"Missing fields: {sorted(missing)}")

    return {
        "event_type": str(event["event_type"]),
        "page": str(event["page"]),
        "user_id": str(event["user_id"]),
    }


def worker_main(worker_id, input_queue, result_queue):
    """
    Process events until a None sentinel is received.

    Each worker sends one final summary to the aggregator.
    """
    event_types = Counter()
    pages = Counter()
    total_events = 0
    invalid_events = 0

    while True:
        item = input_queue.get()

        if item is None:
            break

        try:
            # The consumer may send a JSON string or a decoded dictionary.
            if isinstance(item, str):
                event = json.loads(item)
            else:
                event = item

            parsed = process_event(event)

            event_types[parsed["event_type"]] += 1
            pages[parsed["page"]] += 1
            total_events += 1

        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            invalid_events += 1
            print(f"Worker {worker_id}: rejected event: {exc}")

    # Send exactly one summary per worker.
    result_queue.put({
        "worker_id": worker_id,
        "total_events": total_events,
        "invalid_events": invalid_events,
        "event_types": dict(event_types),
        "pages": dict(pages),
    })

    # Signal that this worker has finished.
    result_queue.put(None)


if __name__ == "__main__":
    print("Import worker_main from consumer.py to start multiprocessing workers.")
