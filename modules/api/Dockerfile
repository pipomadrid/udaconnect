FROM python:3.10-slim

WORKDIR .

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    libgeos-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]
