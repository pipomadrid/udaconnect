import threading
import os
import sys
from app import create_app
from app.kafka.location_consumer import consume

import logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("orquestador")

def run_consumer():
    logger.info("Iniciando el hilo del consumidor...")
    consume()

if __name__ == "__main__":

    consumer_thread = threading.Thread(target=run_consumer, daemon=True)
    consumer_thread.start()

    logger.info("Iniciando el servidor Flask...")
    app = create_app(os.getenv("FLASK_ENV") or "test")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


