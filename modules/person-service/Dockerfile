FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

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
