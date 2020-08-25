FROM python:3

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py src/main.py
CMD python src/main.py
