
import json
import random
import time
import uuid
from datetime import datetime, timezone

from confluent_kafka import Producer


BROKER = "localhost:9092"
TOPIC = "clickstream-events"

PAGES = [
    "/",
    "/products",
    "/about",
    "/contact",
    "/checkout",
]

EVENT_TYPES = [
    "page_view",
    "click",
    "add_to_cart",
    "purchase",
]


def delivery_report(error, message):
    if error is not None:
        print(f"Delivery failed: {error}")
    else:
        print(
            f"Delivered to {message.topic()} "
            f"[partition {message.partition()}] "
            f"offset {message.offset()}"
        )


def main():
    producer = Producer({
        "bootstrap.servers": BROKER,
        "client.id": "task9-clickstream-producer",
    })

    print("Clickstream producer started.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            event = {
                "event_id": str(uuid.uuid4()),
                "user_id": f"user_{random.randint(1, 100)}",
                "event_type": random.choice(EVENT_TYPES),
                "page": random.choice(PAGES),
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
            }

            payload = json.dumps(event).encode("utf-8")

            producer.produce(
                TOPIC,
                key=event["user_id"].encode("utf-8"),
                value=payload,
                callback=delivery_report,
            )

            producer.poll(0)
            print("Produced:", payload.decode("utf-8"))

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping producer...")

    finally:
        producer.flush()
        print("Producer stopped.")


if __name__ == "__main__":
    main()
