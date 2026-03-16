# Connections Microservice

The Connections Microservice is the analytical engine of the UdaConnect ecosystem. It processes location data to identify "connections" (geographic proximity events) between attendees. It operates as an event-driven service, consuming updates from a message broker and exposing processed results via REST.

## Features

- **Kafka Consumer**: Asynchronous processing of location events.
- **REST API**: Exposes connection history and discovered relationships
- **Service Integration**: Communicates via gRPC with the Person microservice to enrich data.

## Ports

- **5000**: Application server port
- **30001** : External access port
- **Kafka Port**: Defined via environment variable (default 9092)

## Structure

```
app/
├── __init__.py           # Flask App Factory & Kafka consumer startup
├── config.py             # Environment configurations (K8s Env vars)
├── kafka_consumer.py     # Background worker for location events
└── connections/
    ├── __init__.py
    ├── models.py         # SQLAlchemy models for Connection records
    ├── schemas.py        # Validation and serialization
    ├── services.py       # Core business logic (Proximity calculations)
    └── routes.py         # RESTful API endpoint definitions
wsgi.py                   # Application entry point
requirements.txt          # Dependencies
Dockerfile                # Container manifest
deployment/
└── connections-deployment.yaml 
```

##  Getting Started

## Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service (Requires Kafka and Postgres/PostGIS)
python wsgi.py
```



## Endpoints REST

### GET /api/persons/<person_id>/connection

Retrieve all recorded connections.

```bash
curl "http://localhost:30001/api/persons/1/connection?start_date=2026-03-01&end_date=2026-03-16&distance=5"

```

## Docker

```bash
# Build

docker build -t connections-service:latest .

```

## Deploying to Cluster


```bash
# Apply the deployment and service manifests
kubectl apply -f deployment/udaconnect-connections.yaml


# Apply the deployment and service manifests of the Kafka consumer
kubectl apply -f deployment/udaconnect-connections-consumer.yaml

```
