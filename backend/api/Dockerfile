FROM python:3.11-slim

WORKDIR /app

# Install PostgreSQL client (psql)
RUN apt-get update && apt-get install -y postgresql-client && apt-get clean

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
COPY utils/ ./utils
COPY sql/ ./sql

EXPOSE 8008

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008", "--reload"]