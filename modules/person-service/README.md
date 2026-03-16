# Person Microservice

Microservice for managing people within the UdaConnect ecosystem. It provides an interface for external clients via REST and internal communication via gRPC.

## Features

- **REST API**: HTTP endpoints for Person CRUD operations.
- **gRPC Server**: Internal service for high-performance communication with ConnectionService.
- **SQLAlchemy ORM**: Database access and management.
- **Flask**: Web framework for the API layer.

## Ports

- **5001**: HTTP/REST API
- **5005**: gRPC Server

## Structure

```
app/
├── __init__.py           # Flask App Factory and initialization
├── config.py             # Environment-based configuration logic
├── grpc_server.py        # Implementation of the gRPC server listener
└── person/
    ├── __init__.py
    ├── models.py         # SQLAlchemy Database models (Person entity)
    ├── schemas.py        # Marshmallow schemas for serialization/validation
    ├── services.py       # Core business logic (CRUD operations)
    ├── routes.py         # RESTful API endpoint definitions
    └── grpc_handler.py   # gRPC service implementation (servicer)
protos/
└── person.proto          # Protocol Buffer definitions
wsgi.py                   # Main entry point for the application
requirements.txt          # Python dependencies
Dockerfile                # Containerization manifest
```

##  Getting Started

## 1. Compile gRPC Definitions

```bash
python -m grpc_tools.protoc \
    -I./protos \
    --python_out=./protos \
    --grpc_python_out=./protos \
    ./protos/person.proto
```

## Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
python wsgi.py
```

## Endpoints REST

### GET /api/persons
Get all persons

```bash
curl http://localhost:5001/api/persons
```

### POST /api/persons
Create new person

```bash
curl -X POST http://localhost:5001/api/persons \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Peter",
    "last_name": "Parker",
    "company_name": "Daily Bugle"
  }'
```

### GET /api/persons/<person_id>
Get person by id
```bash
curl http://localhost:5001/api/persons/1
```

## Internal Communication (gRPC)

The gRPC server facilitates high-speed data exchange with the Connection Service. It implements the following methods:

- `GetPerson(PersonRequest)`: Retrieves person data by ID
- `GetAllPersons(Empty)`: Streams or returns all persons
- `CreatePerson(PersonRequest)`: Internal creation of profiles

## Containerization

```bash
# Build Image
docker build -t person-service:latest .
```

## Deploying to Cluster

```bash
# Apply the deployment and service manifests
kubectl apply -f deployment/udaconnect-person.yaml
```