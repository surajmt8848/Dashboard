FROM python:3.8.3-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
    
# pillow dependencies
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
COPY . /code
