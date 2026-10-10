# Task 9 – Real-Time Clickstream Parsing with Kafka and Multiprocessing

## Project Overview

This project implements a real-time clickstream processing pipeline using Apache Kafka, Python multiprocessing, and JSON. It produces simulated website activity events, streams them through Kafka, processes events using independent worker processes, and aggregates the results.

## Objectives

- Configure a containerized Kafka broker using Docker Compose.
- Generate real-time clickstream events in JSON format.
- Consume events from a Kafka topic using `confluent-kafka`.
- Process events concurrently using Python's `multiprocessing` module.
- Validate incoming events and aggregate event-type and page counts.
- Verify the Python modules and multiprocessing functionality.

## Technology Stack

- Python 3.10+
- Apache Kafka
- Docker and Docker Compose
- confluent-kafka
- Python multiprocessing
- JSON

## Project Structure

```text
Task 9/
├── producer.py
├── consumer.py
├── clickstream_worker.py
├── aggregator.py
├── task9.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Architecture

1. **Producer:** Generates simulated website events.
2. **Kafka:** Receives events in the `clickstream-events` topic.
3. **Consumer:** Reads Kafka messages and dispatches them to worker processes.
4. **Workers:** Validate JSON events and maintain event-type and page counts.
5. **Aggregator:** Combines worker summaries into a consolidated report.
6. **Verification:** Tests imports, JSON parsing, validation, and multiprocessing.

## Installation

Install the Python dependency:

```bash
python -m pip install -r requirements.txt
```

Start Kafka from the project directory:

```bash
docker compose up -d
```

Create the Kafka topic:

```bash
docker exec task9-kafka /opt/kafka/bin/kafka-topics.sh --create --topic clickstream-events --bootstrap-server localhost:9092 --partitions 4 --replication-factor 1
```

If the topic already exists, use the topic-list command to verify it:

```bash
docker exec task9-kafka /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

## Running the Project

Start the consumer in one terminal:

```bash
python consumer.py
```

Start the producer in another terminal:

```bash
python producer.py
```

Stop each program with `Ctrl+C`.

## Run the Aggregator Test

```bash
python aggregator.py
```

## Run Local Verification

```bash
python task9.py
```

### Verification Results

The local verification completed successfully:

| Test | Result |
|---|---|
| Module imports | PASS |
| JSON event parsing | PASS |
| Invalid event validation | PASS |
| Multiprocessing | PASS |
| Total | 4/4 PASS |

## Limitations and Future Improvements

- Implement worker acknowledgements before committing Kafka offsets.
- Handle partition assignments and rebalancing explicitly.
- Add robust recovery for worker failures.
- Improve delivery guarantees and shutdown coordination.
- Add integration tests against the running Kafka broker.

## Conclusion

Task 9 demonstrates a Kafka-based clickstream pipeline with JSON event generation, multiprocessing workers, and aggregation. The local verification suite passed all four tests. Live Kafka reliability and offset-commit guarantees require additional integration testing.
