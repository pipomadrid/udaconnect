FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    libgeos-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*ql-dev

# Copy requirements and install Python dependencies
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Expose ports
# 5001: Flask HTTP
# 50051: gRPC
EXPOSE 5001 50051

COPY . .
# Run the application
CMD ["python", "wsgi.py"]
