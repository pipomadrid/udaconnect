# Person Microservice

Microservicio para la gestión de personas en UdaConnect. Comunica con el exterior mediante HTTP (REST) y con otros microservicios mediante gRPC.

## Características

- **REST API**: Endpoints HTTP para CRUD de personas
- **gRPC Server**: Servicio gRPC para comunicación interna con ConnectionService
- **SQLAlchemy ORM**: Acceso a base de datos
- **Flask**: Framework web

## Puertos

- **5001**: HTTP/REST API
- **50051**: gRPC Server

## Estructura

```
app/
├── __init__.py           # Factory de Flask
├── config.py             # Configuración
├── grpc_server.py        # Servidor gRPC
└── person/
    ├── __init__.py
    ├── models.py         # Modelo de base de datos
    ├── schemas.py        # Schemas de validación (Marshmallow)
    ├── services.py       # Lógica de negocio
    ├── routes.py         # Rutas REST
    └── grpc_handler.py   # Handlers de gRPC
protos/
└── person.proto          # Definiciones de gRPC

wsgi.py                  # Entry point
requirements.txt
Dockerfile
```

## Compilar gRPC

```bash
python -m grpc_tools.protoc \
    -I./protos \
    --python_out=./protos \
    --grpc_python_out=./protos \
    ./protos/person.proto
```

## Ejecutar localmente

```bash
# Instalar dependencias
pip install -r requirements.txt

# Variables de entorno
export DB_USERNAME=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=udaconnect
export FLASK_PORT=5001
export GRPC_PORT=50051

# Ejecutar
python wsgi.py
```

## Endpoints REST

### GET /api/persons
Obtiene todas las personas.

```bash
curl http://localhost:5001/api/persons
```

### POST /api/persons
Crea una nueva persona.

```bash
curl -X POST http://localhost:5001/api/persons \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "company_name": "Acme"
  }'
```

### GET /api/persons/<person_id>
Obtiene una persona por ID.

```bash
curl http://localhost:5001/api/persons/1
```

## gRPC

El servicio implementa los siguientes métodos gRPC:

- `GetPerson(PersonRequest)`: Obtiene una persona por ID
- `GetAllPersons(Empty)`: Obtiene todas las personas
- `CreatePerson(PersonRequest)`: Crea una nueva persona

## Docker

```bash
# Build
docker build -t person-service:latest .

# Run
docker run -p 5001:5001 -p 50051:50051 \
  -e DB_HOST=postgres \
  -e DB_USERNAME=postgres \
  -e DB_PASSWORD=postgres \
  -e DB_NAME=udaconnect \
  person-service:latest
```
