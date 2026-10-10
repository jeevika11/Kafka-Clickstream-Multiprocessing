
import json
import multiprocessing as mp
import queue
import sys

from clickstream_worker import process_event


def worker_test(input_queue, result_queue):
    """Process one JSON event in a child process."""
    try:
        item = input_queue.get(timeout=5)
        event = json.loads(item)
        parsed = process_event(event)
        result_queue.put(("PASS", parsed))
    except Exception as exc:
        result_queue.put(("FAIL", str(exc)))


def main():
    print("=" * 55)
    print("TASK 9 - CLICKSTREAM PIPELINE VERIFICATION")
    print("=" * 55)

    checks = {}

    # 1. Verify imports.
    try:
        import producer
        import consumer
        import aggregator
        import clickstream_worker
        checks["Module imports"] = True
    except Exception as exc:
        print("Import error:", exc)
        checks["Module imports"] = False

    event = {
        "event_id": "test-001",
        "user_id": "user_1",
        "event_type": "page_view",
        "page": "/",
        "timestamp": "2026-10-10T10:00:00+00:00",
    }

    # 2. Verify JSON parsing and event validation.
    try:
        decoded = json.loads(json.dumps(event))
        parsed = process_event(decoded)
        checks["JSON event parsing"] = (
            parsed["event_type"] == "page_view"
            and parsed["page"] == "/"
        )
    except Exception as exc:
        print("JSON error:", exc)
        checks["JSON event parsing"] = False

    # 3. Verify rejection of malformed events.
    try:
        process_event({"event_type": "click"})
        checks["Invalid event validation"] = False
    except ValueError:
        checks["Invalid event validation"] = True

    # 4. Verify multiprocessing with bounded queue waits.
    ctx = mp.get_context("spawn")
    input_queue = ctx.Queue()
    result_queue = ctx.Queue()
    process = ctx.Process(
        target=worker_test,
        args=(input_queue, result_queue),
    )

    try:
        process.start()
        input_queue.put(json.dumps(event))

        process.join(timeout=10)

        if process.is_alive():
            process.terminate()
            process.join(timeout=3)
            checks["Multiprocessing"] = False
        else:
            try:
                status, result = result_queue.get(timeout=3)
                checks["Multiprocessing"] = (
                    status == "PASS"
                    and result["event_type"] == "page_view"
                )
            except queue.Empty:
                checks["Multiprocessing"] = False

    except Exception as exc:
        print("Multiprocessing error:", exc)
        checks["Multiprocessing"] = False

    finally:
        for item in (input_queue, result_queue):
            try:
                item.close()
                item.join_thread()
            except (OSError, ValueError):
                pass

    print("\nVERIFICATION RESULTS")
    print("-" * 55)

    for name, passed in checks.items():
        print(f"{name:<30}: {'PASS' if passed else 'FAIL'}")

    passed_count = sum(checks.values())
    total_count = len(checks)

    print("-" * 55)
    print(f"Tests passed: {passed_count}/{total_count}")

    if passed_count == total_count:
        print("\nTASK 9 LOCAL VERIFICATION: PASS")
    else:
        print("\nTASK 9 LOCAL VERIFICATION: FAIL")
        sys.exit(1)

    print("=" * 55)


if __name__ == "__main__":
    mp.freeze_support()
    main()
