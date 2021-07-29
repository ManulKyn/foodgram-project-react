FROM python:3.8.5
WORKDIR /code
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
WORKDIR ./foodgram
ENV DATABASE_URL psql://foodgram_user:xxxyyyzzz@127.0.0.1:5432/foodgram
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000