FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt .

ENV PYTHONPATH=/app

RUN pip install --upgrade pip \ 
  && pip install --no-cache-dir -r requirements.txt gunicorn

COPY . /app

RUN ls -R /app

EXPOSE 8000

ENV FLASK_APP=app.py 
ENV FLASK_RUN_HOST=0.0.0.0 
ENV FLASK_RUN_PORT=8000 

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]