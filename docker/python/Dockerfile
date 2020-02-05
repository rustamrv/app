FROM python:3.6
MAINTAINER shop@localhost

COPY ./app /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]