import logging
from concurrent import futures

import grpc

from app.person.grpc_handler import PersonServicer
from protos import person_pb2_grpc

logger = logging.getLogger("person-service")


def serve(port: int = 5005):
    """Start the gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    
    logger.info(f"Starting gRPC server on port {port}")
    server.start()
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Stopping gRPC server")
        server.stop(0)

if __name__ == "__main__":
    serve()
