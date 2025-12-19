FROM python:3.11-slim
WORKDIR /app
ENV PYTHONPATH=/app:$PYTHONPATH
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD alembic upgrade head && fastapi dev main.py --host 0.0.0.0 --port 8000

