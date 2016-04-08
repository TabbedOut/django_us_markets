FROM python:2.7

RUN apt-get update
RUN apt-get install -y binutils libproj-dev gdal-bin libpq-dev python-pip

RUN pip install "Django<1.8"
RUN pip install "psycopg2<3"
RUN pip install "csvkit<1"
RUN pip install ipdb

COPY . /app
WORKDIR /app
ENV PYTHONPATH /app
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE tests.settings

ENTRYPOINT ["django-admin"]
