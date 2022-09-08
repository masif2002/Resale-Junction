FROM python:3.8.13-slim-buster

RUN mkdir -p /home/django/mysite \
    && mkdir -pv /var/log/gunicorn \
    && mkdir -pv /var/run/gunicorn

WORKDIR /home/django/mysite

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN pip install -r requirements.txt 

COPY . .

CMD ["gunicorn", "-c", "config/gunicorn/dev.py"]