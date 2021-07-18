FROM python:3.8.5
WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt
CMD gunicorn backend.foodgram.wsgi:application --bind 0.0.0.0:8000