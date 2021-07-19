FROM python:3.8.5
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /code
COPY frontend/package*.json ./
CMD gunicorn backend.foodgram.wsgi:application --bind 0.0.0.0:8000