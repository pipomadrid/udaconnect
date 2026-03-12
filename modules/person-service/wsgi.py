import os
import logging
import threading
from app import create_app
from app.grpc_server import serve

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("person-service")

# Create Flask app
app = create_app()

# Start gRPC server in a separate thread
def start_grpc():
    """Start gRPC server in background."""
    grpc_port = int(os.getenv("GRPC_PORT", 5005))
    logger.info(f"Starting gRPC server on port {grpc_port}")
    serve(port=grpc_port)

if __name__ == "__main__":
    # Start gRPC server in background thread
    grpc_thread = threading.Thread(target=start_grpc, daemon=True)
    grpc_thread.start()
    
    # Start Flask app
    flask_port = int(os.getenv("FLASK_PORT", 5001))
    flask_debug = os.getenv("FLASK_DEBUG", False)
    
    logger.info(f"Starting Flask server on port {flask_port}")
    app.run(host="0.0.0.0", port=flask_port, debug=flask_debug, use_reloader=False)
