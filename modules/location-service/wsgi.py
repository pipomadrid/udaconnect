import os

from app import create_app

app = create_app(os.getenv("FLASK_ENV") or "test")
if __name__ == "__main__":
    app.run(debug=True)
    
    logger.info(f"Starting Flask server on port {flask_port}")
    app.run(host="0.0.0.0", port=flask_port, debug=flask_debug, use_reloader=False)
