FROM python:3.11.6

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY req.txt .

RUN pip install -r req.txt

COPY . .


RUN alembic upgrade head

WORKDIR src

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
