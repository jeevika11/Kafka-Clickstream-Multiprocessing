
import multiprocessing as mp
import signal

from confluent_kafka import Consumer, KafkaError

from clickstream_worker import worker_main
from aggregator import aggregate_results, print_summary


BROKER = "localhost:9092"
TOPIC = "clickstream-events"
GROUP_ID = "task9-clickstream-consumer"
WORKER_COUNT = 4


def main():
    ctx = mp.get_context("spawn")
    input_queues = [ctx.Queue() for _ in range(WORKER_COUNT)]
    result_queue = ctx.Queue()

    workers = [
        ctx.Process(
            target=worker_main,
            args=(worker_id, input_queues[worker_id], result_queue),
            name=f"ClickstreamWorker-{worker_id}",
        )
        for worker_id in range(WORKER_COUNT)
    ]

    for worker in workers:
        worker.start()

    consumer = Consumer({
        "bootstrap.servers": BROKER,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    })

    stopping = False
    dispatched = 0

    def request_stop(signum, frame):
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGINT, request_stop)

    try:
        consumer.subscribe([TOPIC])
        print(f"Subscribed to {TOPIC}.")
        print(f"Started {WORKER_COUNT} worker processes.")
        print("Press Ctrl+C to stop.\n")

        while not stopping:
            message = consumer.poll(1.0)

            if message is None:
                continue

            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    continue
                print("Kafka error:", message.error())
                continue

            # Dispatch records round-robin to independent workers.
            worker_index = dispatched % WORKER_COUNT
            input_queues[worker_index].put(message.value())
            dispatched += 1

            # Commit only after the worker finishes and acknowledges
            # its events in a future production-grade implementation.
            # This basic demonstration commits after dispatch.
            consumer.commit(message=message, asynchronous=False)

            if dispatched % 20 == 0:
                print(f"Dispatched {dispatched} events.")

    finally:
        print("\nStopping consumer...")
        consumer.close()

        # Signal every worker to finish its assigned events.
        for queue in input_queues:
            queue.put(None)

        # Wait for worker summaries to be generated.
        for worker in workers:
            worker.join(timeout=10)

        # Ensure a stuck process cannot keep the program alive.
        for worker in workers:
            if worker.is_alive():
                worker.terminate()
                worker.join()

        summary = aggregate_results(result_queue, WORKER_COUNT)
        print_summary(summary)

        for queue in input_queues:
            queue.close()
        result_queue.close()


if __name__ == "__main__":
    mp.freeze_support()
    main()
