
FROM python:3.8.5

RUN mkdir /code

COPY requirements.txt /code

RUN pip install -r /code/requirements.txt

LABEL author_github='https://github.com/olifirovai' author_email='i.s.olifirova@gmail.com' version=1

COPY . /code

WORKDIR /code

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
