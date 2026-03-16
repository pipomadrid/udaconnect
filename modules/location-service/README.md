# Location Microservice

The Location Microservice is the primary data ingestion point for the UdaConnect ecosystem. It is designed to handle high-frequency GPS coordinate updates from mobile devices (UdaTracker) and persist them into a spatial database for real-time analysis.

## Features

- **Kafka producer**: Optionally publishes verified location events to the message broker for downstream processing by the Connections service.
- **REST API**: Exposes connection history and discovered relationships
- **Service Integration**: Communicates via gRPC with the Person microservice to enrich data.

## Ports

- **5002**: Application server port
- **30003** : External access port

## Structure

```
app/
├── __init__.py           # Flask App Factory
├── config.py             # Infrastructure & K8s environment settings
├── kafka_producer.py     # Logic for pushing events to the message bus
└── location/
    ├── __init__.py
    ├── models.py         # SQLAlchemy/GeoAlchemy2 models
    ├── schemas.py        # Marshmallow validation schemas
    ├── services.py       # Persistence & Spatial validation logic
    └── routes.py         # RESTful API ingestion endpoints
wsgi.py                   # Application entry point
requirements.txt          # Python dependencies
Dockerfile                # Container manifest
deployment/
└── location-deployment.yaml 
```

##  Getting Started

## Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service 
python wsgi.py
```



## Endpoints REST

### POST /api/locations

Accepts raw GPS data from tracking devices.

```bash
curl -X POST http://localhost:30003/api/locations \
  -H "Content-Type: application/json" \
  -d '{
    "person_id": 1,
    "longitude": -122.4194,
    "latitude": 37.7749,
    "coordinate_time": "2026-03-16T13:00:00Z"
  }'

```
### GET /api/locations/<person_id>

Retrieves the location history for a specific person via the NodePort.

```bash
curl http://localhost:30003/api/locations/1

```


## Docker

```bash
# Build

docker build -t location-service:latest .
```

## Deploying to Cluster


```bash
# Apply the deployment and service manifests
kubectl apply -f deployment/udaconnect-location.yaml
```
